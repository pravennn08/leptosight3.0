import bcrypt
import json
from datetime import datetime, timedelta, timezone
from .config.connect_db import connect_db


class AdminDatabaseService:
    def __init__(self):
        self.user_table = "users"
        self.diagnostic_table = "diagnostic"
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

        self.current_user = None

    # FETCH TOTAL USER, DIAGNOSTICS, SEVERE RISK CASES, LAST ACTIVITY(USED UPDATED AT FROM USERS TABLE )
    def fetch_admin_stats(self):
        try:
            with self.conn.cursor() as cur:

                # 🔥 MAIN QUERY
                query = f"""
                SELECT
                    (SELECT COUNT(*) FROM {self.user_table}) AS total_users,

                    (SELECT COUNT(*) FROM {self.diagnostic_table}) AS total_test,

                    (SELECT COUNT(*) 
                    FROM {self.diagnostic_table} 
                    WHERE LOWER(risk_level) = 'severe') AS severe_cases,

                    (SELECT MAX(updated_at) FROM {self.user_table}) AS last_activity
                """

                cur.execute(query)
                result = cur.fetchone()

            if not result:
                return None

            total_users, total_test, severe_cases, last_activity = result

            def time_ago(dt):
                if not dt:
                    return "No activity"

                now = datetime.now(dt.tzinfo)
                diff = now - dt

                seconds = int(diff.total_seconds())

                if seconds < 60:
                    return "Just now"
                elif seconds < 3600:
                    mins = seconds // 60
                    return f"{mins} minute{'s' if mins > 1 else ''} ago"
                elif seconds < 86400:
                    hours = seconds // 3600
                    return f"{hours} hour{'s' if hours > 1 else ''} ago"
                else:
                    days = seconds // 86400
                    return f"{days} day{'s' if days > 1 else ''} ago"

            return {
                "total_users": total_users or 0,
                "total_test": total_test or 0,
                "severe_cases": severe_cases or 0,
                "last_activity": time_ago(last_activity),
            }

        except Exception as error:
            print("FETCH ADMIN STATS ERROR:", error)
            return None

    # FETCH NEW USERS WEEKLY
    def fetch_weekly_users(self):
        try:
            with self.conn.cursor() as cur:

                query = f"""
                SELECT 
                    EXTRACT(DOW FROM created_at) AS dow,
                    COUNT(*) AS total
                FROM {self.user_table}
                WHERE created_at >= NOW() - INTERVAL '7 days'
                GROUP BY dow
                ORDER BY dow
                """

                cur.execute(query)
                rows = cur.fetchall()

            # =========================
            # MAP DOW → DAY NAME
            # PostgreSQL: 0=Sunday ... 6=Saturday
            # =========================
            dow_map = {
                0: "Sun",
                1: "Mon",
                2: "Tue",
                3: "Wed",
                4: "Thu",
                5: "Fri",
                6: "Sat",
            }

            # Initialize all days = 0
            weekly_data = {
                "Mon": 0,
                "Tue": 0,
                "Wed": 0,
                "Thu": 0,
                "Fri": 0,
                "Sat": 0,
                "Sun": 0,
            }

            # Fill from DB
            for dow, count in rows:
                day_name = dow_map[int(dow)]
                weekly_data[day_name] = count

            # ✅ ORDER (Mon → Sun)
            ordered = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

            return [{"day": day, "users": weekly_data[day]} for day in ordered]

        except Exception as error:
            print("FETCH WEEKLY USERS ERROR:", error)
            return None

    # FETCH RISK LEVEL IN DIAGNOSIS TABLE
    def fetch_risk_level(self):
        try:
            with self.conn.cursor() as cur:

                query = f"""
                SELECT LOWER(risk_level) AS level, COUNT(*) AS total
                FROM {self.diagnostic_table}
                GROUP BY LOWER(risk_level)
                """

                cur.execute(query)
                rows = cur.fetchall()

            # =========================
            # DEFAULT VALUES (IMPORTANT)
            # =========================
            risk_map = {
                "safe": 0,
                "mild": 0,
                "moderate": 0,
                "severe": 0,
            }

            # Fill from DB
            for level, count in rows:
                if level in risk_map:
                    risk_map[level] = count

            # =========================
            # FORMAT FOR CHART
            # =========================
            return [
                {"classification": "Safe", "value": risk_map["safe"]},
                {"classification": "Mild", "value": risk_map["mild"]},
                {"classification": "Moderate", "value": risk_map["moderate"]},
                {"classification": "Severe", "value": risk_map["severe"]},
            ]

        except Exception as error:
            print("FETCH RISK LEVEL ERROR:", error)
            return None

    def fetch_all_users(self):
        try:
            with self.conn.cursor() as cur:

                query = f"""
                SELECT 
                    id,
                    name,
                    email,
                    phone_number,
                    password,
                    role,
                    is_verified,
                    last_login_at,
                    created_at,
                    updated_at
                FROM {self.user_table}
                ORDER BY created_at DESC
                """

                cur.execute(query)
                rows = cur.fetchall()

            if not rows:
                return []

            results = []

            for row in rows:
                (
                    user_id,
                    name,
                    email,
                    phone,
                    password,
                    role,
                    is_verified,
                    last_login,
                    created_at,
                    updated_at,
                ) = row

                # =========================
                # DISPLAY (TABLE SAFE)
                # =========================
                role_text = role.capitalize() if role else "N/A"
                status = "Verified" if is_verified else "Pending"

                display = (
                    user_id,
                    email,
                    phone,
                    role_text,
                    status,
                    "View",
                )

                # =========================
                # FULL (FOR MODAL)
                # =========================
                full = {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    "phone_number": phone,
                    "password": password,
                    "role": role,
                    "is_verified": is_verified,
                    "last_login_at": last_login,
                    "created_at": created_at,
                    "updated_at": updated_at,
                }

                results.append(
                    {
                        "id": user_id,
                        "display": display,
                        "full": full,
                    }
                )

            return results

        except Exception as error:
            print("FETCH USERS ERROR:", error)
            return None

    def filter_users(self, keyword="", role="All", status="All"):
        try:
            with self.conn.cursor() as cur:

                query = f"""
                SELECT 
                    id,
                    name,
                    email,
                    phone_number,
                    password,
                    role,
                    is_verified,
                    last_login_at,
                    created_at,
                    updated_at
                FROM {self.user_table}
                WHERE 1=1
                """

                params = []

                # =========================
                # 🔍 SEARCH
                # =========================
                if keyword:
                    query += """
                    AND (
                        id::text ILIKE %s OR
                        name ILIKE %s OR
                        email ILIKE %s OR
                        phone_number ILIKE %s OR
                        role::text ILIKE %s OR
                        (
                            CASE 
                                WHEN is_verified = TRUE THEN 'verified'
                                ELSE 'pending'
                            END
                        ) ILIKE %s
                    )
                    """
                    like = f"%{keyword}%"
                    params.extend([like, like, like, like, like, like])

                # =========================
                # 👤 ROLE FILTER
                # =========================
                if role.lower() != "all":
                    query += " AND role::text = %s"
                    params.append(role.lower())

                # =========================
                # ✅ STATUS FILTER
                # =========================
                if status.lower() != "all":
                    is_verified = True if status.lower() == "verified" else False
                    query += " AND is_verified = %s"
                    params.append(is_verified)

                query += " ORDER BY created_at DESC"

                cur.execute(query, tuple(params))
                rows = cur.fetchall()

            if not rows:
                return []

            results = []

            for row in rows:
                (
                    user_id,
                    name,
                    email,
                    phone,
                    password,
                    role,
                    is_verified,
                    last_login,
                    created_at,
                    updated_at,
                ) = row

                role_text = role.capitalize() if role else "N/A"
                status_text = "Verified" if bool(is_verified) else "Pending"

                display = (
                    user_id,
                    email,
                    phone,
                    role_text,
                    status_text,
                    "View",
                )

                full = {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    "phone_number": phone,
                    "password": password,
                    "role": role,
                    "is_verified": is_verified,
                    "last_login_at": last_login,
                    "created_at": created_at,
                    "updated_at": updated_at,
                }

                results.append(
                    {
                        "id": user_id,
                        "display": display,
                        "full": full,
                    }
                )

            return results

        except Exception as error:
            self.conn.rollback()
            print("FILTER USERS ERROR:", error)
            return None

    def update_user(
        self,
        user_id,
        name,
        email,
        phone_number,
        role,
        is_verified,
    ):
        try:
            with self.conn.cursor() as cur:

                # =========================
                # 🔥 DUPLICATE CHECK
                # =========================
                check_query = f"""
                SELECT email, phone_number
                FROM {self.user_table}
                WHERE (email = %s OR phone_number = %s)
                AND id != %s
                """

                cur.execute(check_query, (email, phone_number, user_id))
                existing = cur.fetchone()

                if existing:
                    existing_email, existing_phone = existing

                    if existing_email == email:
                        return "EMAIL_EXISTS"

                    if existing_phone == phone_number:
                        return "PHONE_EXISTS"

                    return "DUPLICATE"

                # =========================
                # ✅ UPDATE USER
                # =========================
                update_query = f"""
                UPDATE {self.user_table}
                SET 
                    name = %s,
                    email = %s,
                    phone_number = %s,
                    role = %s,
                    is_verified = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING id
                """

                cur.execute(
                    update_query,
                    (
                        name,
                        email,
                        phone_number,
                        role,
                        is_verified,
                        user_id,
                    ),
                )

                updated = cur.fetchone()

            self.conn.commit()

            if not updated:
                return "USER_NOT_FOUND"

            return "USER_UPDATED"

        except Exception as error:
            print("UPDATE USER ERROR:", error)
            return "ERROR"

    def add_account(self, data):
        try:
            with self.conn.cursor() as cur:

                # =========================
                # 🔥 DUPLICATE CHECK
                # =========================
                check_query = f"""
                SELECT email, phone_number
                FROM {self.user_table}
                WHERE email = %s OR phone_number = %s
                """

                cur.execute(check_query, (data.email, data.phone_number))
                existing = cur.fetchone()

                if existing:
                    existing_email, existing_phone = existing

                    if existing_email == data.email:
                        return "EMAIL_EXISTS"

                    if existing_phone == data.phone_number:
                        return "PHONE_EXISTS"

                    return "DUPLICATE"

                # =========================
                # 🔐 HASH PASSWORD
                # =========================
                hashed = bcrypt.hashpw(
                    data.password.encode(), bcrypt.gensalt()
                ).decode()

                # =========================
                # OPTIONAL OTP (can be None)
                # =========================
                otp_code = None
                otp_expiry = None

                # =========================
                # INSERT USER
                # =========================
                query = f"""
                INSERT INTO {self.user_table}
                (name, email, phone_number, password, role, is_verified, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING id
                """

                cur.execute(
                    query,
                    (
                        data.name,
                        data.email,
                        data.phone_number,
                        hashed,
                        data.role,
                        data.is_verified,
                    ),
                )

                user = cur.fetchone()

            self.conn.commit()

            return user if user else "ERROR"

        except Exception as error:
            print("ADD USER ERROR:", error)
            return "ERROR"

    def delete_user(self, id):
        try:
            with self.conn.cursor() as cur:

                # ✅ check if exists
                cur.execute(
                    f"SELECT id FROM {self.user_table} WHERE id = %s",
                    (id,),
                )
                if not cur.fetchone():
                    return "USER_NOT_FOUND"

                # ✅ delete
                cur.execute(
                    f"DELETE FROM {self.user_table} WHERE id = %s",
                    (id,),
                )

            self.conn.commit()
            return "USER_DELETED"

        except Exception as error:
            print("DELETE USER ERROR:", error)
            return "ERROR"

    def fetch_all_records(self):
        try:
            with self.conn.cursor() as cur:

                query = f"""
                SELECT
                    q.id,
                    q.patient_id,
                    u.name,
                    u.phone_number,
                    q.temp,
                    q.test_classification,
                    q.test_confidence,
                    q.eye_classification,
                    q.eye_confidence,
                    q.risk_level,
                    q.recommendation,
                    q.created_at,
                    q.answers,
                    q.top_patient_factors,
                    q.pdf_path,
                    q.eye_image_path,
                    q.eye_scan_path
                FROM {self.diagnostic_table} q
                JOIN {self.user_table} u
                ON q.patient_id = u.id
                ORDER BY q.created_at DESC
                """

                cur.execute(query)
                rows = cur.fetchall()

            if not rows:
                return []

            results = []

            for row in rows:
                (
                    diagnostic_id,
                    patient_id,
                    name,
                    phone,
                    temp,
                    test_class,
                    test_conf,
                    eye_class,
                    eye_conf,
                    risk_level,
                    recommendation,
                    created_at,
                    answers,
                    factors,
                    pdf_path,
                    eye_img,
                    eye_scan,
                ) = row

                # =========================
                # DISPLAY (TABLE)
                # =========================
                display = (
                    diagnostic_id,
                    f"{temp}°C" if temp is not None else "N/A",
                    test_class or "N/A",
                    eye_class or "N/A",
                    risk_level or "N/A",
                    "Print",  # action button
                )

                # =========================
                # FULL (MODAL + PRINT)
                # =========================
                # full = {
                #     "id": diagnostic_id,
                #     "patient_id": patient_id,
                #     "patient_name": name,
                #     "contact_number": phone,
                #     "temperature": temp,
                #     "test_result": test_class,
                #     "test_conf": test_conf,
                #     "eye_classification": eye_class,
                #     "eye_conf": (
                #         round(float(eye_conf), 2) if eye_conf is not None else 0
                #     ),
                #     "risk_level": risk_level,
                #     "recommendation": recommendation,
                #     "created_at": created_at,
                # }
                full = {
                    "id": diagnostic_id,
                    "patient_id": patient_id,
                    "patient_name": name,
                    "contact_number": phone,
                    "temperature": temp,
                    "test_result": test_class,
                    "test_conf": test_conf,
                    "eye_classification": eye_class,
                    "eye_conf": (
                        round(float(eye_conf), 2) if eye_conf is not None else 0
                    ),
                    "risk_level": risk_level,
                    "recommendation": recommendation,
                    "created_at": created_at,
                    "answers": answers or [],
                    "factors": factors or [],
                    "pdf_path": pdf_path,
                    "eye_image": eye_img,
                    "eye_scan": eye_scan,
                }

                results.append(
                    {
                        "id": diagnostic_id,
                        "display": display,
                        "full": full,
                    }
                )

            return results

        except Exception as error:
            self.conn.rollback()
            print("FETCH RECORDS ERROR:", error)
            return None

    def filter_records(
        self,
        keyword="",
        test_class="All",
        eye_class="All",
        risk_level="All",
    ):
        try:
            with self.conn.cursor() as cur:

                query = f"""
                SELECT
                    q.id,
                    q.patient_id,
                    u.name,
                    u.phone_number,
                    q.temp,
                    q.test_classification,
                    q.test_confidence,
                    q.eye_classification,
                    q.eye_confidence,
                    q.risk_level,
                    q.recommendation,
                    q.created_at,
                    q.answers,
                    q.top_patient_factors,
                    q.pdf_path,
                    q.eye_image_path,
                    q.eye_scan_path
                FROM {self.diagnostic_table} q
                JOIN {self.user_table} u
                ON q.patient_id = u.id
                WHERE 1=1
                """

                params = []

                # =========================
                # 🔍 SEARCH (DISPLAY-BASED)
                # =========================
                if keyword:
                    query += """
                    AND (
                        q.id::text ILIKE %s OR
                        q.temp::text ILIKE %s OR
                        q.test_classification ILIKE %s OR
                        q.eye_classification ILIKE %s OR
                        q.risk_level ILIKE %s
                    )
                    """
                    like = f"%{keyword}%"
                    params.extend([like, like, like, like, like])

                # =========================
                # 🧪 TEST CLASS FILTER
                # =========================
                if test_class.lower() != "all":
                    query += " AND q.test_classification ILIKE %s"
                    params.append(test_class)

                # =========================
                # 👁 EYE CLASS FILTER
                # =========================
                if eye_class.lower() != "all":
                    query += " AND q.eye_classification ILIKE %s"
                    params.append(eye_class)

                # =========================
                # ⚠️ RISK LEVEL FILTER
                # =========================
                if risk_level.lower() != "all":
                    query += " AND q.risk_level ILIKE %s"
                    params.append(risk_level)

                query += " ORDER BY q.created_at DESC"

                cur.execute(query, tuple(params))
                rows = cur.fetchall()

            if not rows:
                return []

            results = []

            for row in rows:
                (
                    diagnostic_id,
                    patient_id,
                    name,
                    phone,
                    temp,
                    test_class,
                    test_conf,
                    eye_class,
                    eye_conf,
                    risk_level,
                    recommendation,
                    created_at,
                    answers,
                    factors,
                    pdf_path,
                    eye_img,
                    eye_scan,
                ) = row

                # =========================
                # DISPLAY
                # =========================
                display = (
                    diagnostic_id,
                    f"{temp}°C" if temp is not None else "N/A",
                    test_class or "N/A",
                    eye_class or "N/A",
                    risk_level or "N/A",
                    "Print",
                )

                # =========================
                # FULL
                # =========================
                full = {
                    "id": diagnostic_id,
                    "patient_id": patient_id,
                    "patient_name": name,
                    "contact_number": phone,
                    "temperature": temp,
                    "test_result": test_class,
                    "test_conf": test_conf,
                    "eye_classification": eye_class,
                    "eye_conf": (
                        round(float(eye_conf), 2) if eye_conf is not None else 0
                    ),
                    "risk_level": risk_level,
                    "recommendation": recommendation,
                    "created_at": created_at,
                    # extra fields
                    "answers": answers or [],
                    "factors": factors or [],
                    "pdf_path": pdf_path,
                    "eye_image": eye_img,
                    "eye_scan": eye_scan,
                }

                results.append(
                    {
                        "id": diagnostic_id,
                        "display": display,
                        "full": full,
                    }
                )

            return results

        except Exception as error:
            self.conn.rollback()
            print("FILTER RECORDS ERROR:", error)
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()
