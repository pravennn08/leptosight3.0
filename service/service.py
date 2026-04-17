import bcrypt
import json
from datetime import datetime, timedelta, timezone
from .config.connect_db import connect_db
from sms.otpTemplate import send_otp_template
from utils.generateOTP import generate_code
from .rate_limit_service import RateLimitService
from .models.user_model import User
from .models.diagnostic_model import Diagnostic


class DatabaseService:
    def __init__(self):
        self.user_table = "users"
        self.diagnostic_table = "diagnostic"
        self.conn = connect_db()
        self.cursor = self.conn.cursor()
        self.rate_limit = RateLimitService()
        self.current_user = None

    # REGISTER USER
    def register(self, data: User, action="register"):

        # RATE LIMIT CHECK
        limit = self.rate_limit.check_rate_limit(
            action=action,
            identifier=data.email.lower(),
            max_attempts=3,
            lock_minutes=15,
        )

        if not limit["allowed"]:
            return {
                "status": "RATE_LIMITED",
                "remaining": limit.get("remaining_seconds", 0),
            }
        try:
            with self.conn.cursor() as cur:
                # Check Duplicates
                check_query = f"""
                SELECT email, phone_number
                FROM {self.user_table}
                WHERE email = %s OR phone_number = %s
                """
                cur.execute(check_query, (data.email, data.phone_number))
                existing = cur.fetchone()

                if existing:
                    return "USER_EXISTS"

                hashed = bcrypt.hashpw(
                    data.password.encode(), bcrypt.gensalt()
                ).decode()

                otp_code = str(generate_code())
                otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=3)

                insert_query = f"""
                INSERT INTO {self.user_table}
                (name, email, phone_number, password, role, otp_code, otp_expires_at, is_verified)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name, email, phone_number
                """

                cur.execute(
                    insert_query,
                    (
                        data.name,
                        data.email,
                        data.phone_number,
                        hashed,
                        data.role,
                        otp_code,
                        otp_expiry,
                        False,
                    ),
                )

                user = cur.fetchone()

            self.conn.commit()

            self.current_user = user

            PHONE_NUM_DEV = "639628456672"
            send_otp_template(PHONE_NUM_DEV, otp_code)

            return user

        except Exception as error:
            print("REGISTER ERROR:", error)
            return None

    # VERIFY OTP
    def verify_otp(self, phone_number, otp):

        # CHECK IF LOCKED
        lock = self.rate_limit.is_locked(
            action="verify_otp",
            identifier=phone_number,
        )

        if lock["locked"]:
            return {
                "status": "RATE_LIMITED",
                "remaining": lock["remaining"],
            }

        try:
            query = f"""
            SELECT otp_code, otp_expires_at, recovery_setup
            FROM {self.user_table}
            WHERE phone_number = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (phone_number,))
                result = cur.fetchone()

            if not result:
                return "USER_NOT_FOUND"

            db_otp, expiry, recovery_setup = result

            # SAFETY CHECK
            if not expiry:
                return "OTP_EXPIRED"

            if datetime.now(timezone.utc) > expiry:
                return "OTP_EXPIRED"

            # WRONG OTP → increment rate limit
            if db_otp != otp:

                self.rate_limit.check_rate_limit(
                    action="verify_otp",
                    identifier=phone_number,
                    max_attempts=5,
                    lock_minutes=2,
                )

                return "INVALID_OTP"

            # SUCCESS → verify user
            update_query = f"""
            UPDATE {self.user_table}
            SET is_verified = TRUE,
                otp_code = NULL,
                otp_expires_at = NULL,
                last_otp_verified_at = NOW()
            WHERE phone_number = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(update_query, (phone_number,))

            self.conn.commit()

            # RESET RATE LIMIT
            self.rate_limit.reset_rate_limit("verify_otp", phone_number)

            # CHECK IF RECOVERY SETUP IS REQUIRED
            if not recovery_setup:
                return "SETUP_RECOVERY_REQUIRED"

            return "VERIFIED"

        except Exception as error:
            print("VERIFY OTP ERROR:", error)
            return "ERROR"

    # RESEND OTP
    def resend_otp(self, phone_number):
        try:
            otp_code = str(generate_code())
            otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=3)

            query = f"""
            UPDATE {self.user_table}
            SET otp_code = %s,
                otp_expires_at = %s
            WHERE phone_number = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (otp_code, otp_expiry, phone_number))

            self.conn.commit()

            PHONE_NUM_DEV = "639628456672"
            send_otp_template(PHONE_NUM_DEV, otp_code)

            return True

        except Exception as error:
            print(error)
            return False

    # RECOVERY QUESTIONS
    def save_recovery_questions(self, email, city, mother_name, birthday):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    f"""
                    UPDATE {self.user_table}
                    SET recovery_city = %s,
                        recovery_mother_name = %s,
                        recovery_birthday = %s,
                        recovery_setup = TRUE
                    WHERE email = %s
                    RETURNING id
                    """,
                    (city, mother_name, birthday, email),
                )

                updated = cur.fetchone()

            self.conn.commit()

            if not updated:
                return "USER_NOT_FOUND"

            return "RECOVERY_SAVED"

        except Exception as e:
            print("RECOVERY SETUP ERROR:", e)
            return "ERROR"

    # LOGIN USER
    def login(self, email, password):

        email = email.lower().strip()
        # CHECK IF LOCKED FIRST
        lock = self.rate_limit.is_locked(
            action="login",
            identifier=email,
        )

        if lock["locked"]:
            return {
                "status": "RATE_LIMITED",
                "remaining": lock["remaining"],
            }

        try:
            query = f"""
            SELECT id, name, email, phone_number, password, role, created_at,
            is_verified, recovery_setup, last_login_at, otp_expires_at
            FROM {self.user_table}
            WHERE email = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (email,))
                user = cur.fetchone()

            if not user:
                return "USER_NOT_FOUND"

            db_password = user[4]
            if isinstance(db_password, str):
                db_password = db_password.encode()

            is_verified = user[7]
            recovery_setup = user[8]

            # WRONG PASSWORD → increment limiter
            if not bcrypt.checkpw(password.encode(), db_password):

                self.rate_limit.check_rate_limit(
                    action="login",
                    identifier=email,
                    max_attempts=5,
                    lock_minutes=5,
                )

                return "INVALID_PASSWORD"

            # SUCCESS → reset limiter
            self.rate_limit.reset_rate_limit("login", email)

            otp_expires_at = user[9]  # adjust index if needed
            now = datetime.now(timezone.utc)

            if not is_verified:
                phone_number = user[3]

                # 🔥 resend only if expired or missing
                if not otp_expires_at or otp_expires_at < now:
                    self.generate_and_send_otp(phone_number)

                self.current_user = user
                return "NOT_VERIFIED"

            if not recovery_setup:
                self.current_user = user
                return "RECOVERY_SETUP_REQUIRED"

            update_query = f"""
            UPDATE {self.user_table}
            SET last_login_at = NOW()
            WHERE email = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(update_query, (email,))

            self.conn.commit()

            self.current_user = user
            return "LOGIN_SUCCESS"

        except Exception as error:
            print("LOGIN ERROR:", error)
            return "ERROR"

    # GENERATE NEW OTP IF EXPIRED
    def generate_and_send_otp(self, phone_number):
        try:
            otp_code = str(generate_code())
            otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=3)

            query = f"""
            UPDATE {self.user_table}
            SET otp_code = %s,
                otp_expires_at = %s
            WHERE phone_number = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (otp_code, otp_expiry, phone_number))

            self.conn.commit()

            PHONE_NUM_DEV = "639628456672"
            send_otp_template(PHONE_NUM_DEV, otp_code)

            return True

        except Exception as error:
            print(error)
            return False

    # FORGOT PASSWORD
    def forgot_password(self, email):

        # RATE LIMIT
        rate = self.rate_limit.check_rate_limit(
            action="forgot_password",
            identifier=email,
            max_attempts=3,
            lock_minutes=5,
        )

        if not rate["allowed"]:
            return {
                "status": "RATE_LIMITED",
                "remaining": rate["remaining_seconds"],
            }

        try:
            query = f"""
            SELECT id, name, email, phone_number
            FROM {self.user_table}
            WHERE email = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (email,))
                user = cur.fetchone()

            if not user:
                return "USER_NOT_FOUND"

            phone_number = user[3]

            # GENERATE OTP
            otp_code = str(generate_code())
            otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=3)

            update_query = f"""
            UPDATE {self.user_table}
            SET otp_code = %s,
                otp_expires_at = %s
            WHERE email = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(update_query, (otp_code, otp_expiry, email))

            self.conn.commit()

            # SEND OTP
            PHONE_NUM_DEV = "639628456672"
            send_otp_template(PHONE_NUM_DEV, otp_code)

            # RESET RATE LIMIT (success)
            self.rate_limit.reset_rate_limit("forgot_password", email)

            # SAVE RECOVERY SESSION (NOT LOGIN SESSION)
            self.recovery_user = user

            return {
                "status": "OTP_SENT",
                "user": user,
            }

        except Exception as e:
            print("FORGOT PASSWORD ERROR:", e)
            return "ERROR"

    # RECOVERY PASSWORD VERIFY OTP
    def recovery_password(self, phone_number, otp):
        # RATE LIMIT
        rate = self.rate_limit.check_rate_limit(
            action="recovery_otp",
            identifier=phone_number,
            max_attempts=5,
            lock_minutes=5,
        )

        if not rate["allowed"]:
            return {
                "status": "RATE_LIMITED",
                "remaining": rate["remaining_seconds"],
            }

        try:
            query = f"""
            SELECT otp_code, otp_expires_at
            FROM {self.user_table}
            WHERE phone_number = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (phone_number,))
                result = cur.fetchone()

            if not result:
                return "USER_NOT_FOUND"

            db_otp, expiry = result

            if datetime.now(timezone.utc) > expiry:
                return "OTP_EXPIRED"

            if db_otp != otp:
                return "INVALID_OTP"

            # SUCCESS → reset limiter
            self.rate_limit.reset_rate_limit("recovery_otp", phone_number)

            return "VERIFIED"

        except Exception as e:
            print("RECOVERY OTP ERROR:", e)
            return "ERROR"

    # VERIFY RECOVERY QUESTIONS
    def verify_recovery_question(self, email, city, mother_name, birthday):

        # CHECK LOCK FIRST
        lock = self.rate_limit.is_locked(
            action="recovery_questions",
            identifier=email,
        )

        if lock["locked"]:
            return {
                "status": "RATE_LIMITED",
                "remaining": lock["remaining"],
            }

        try:
            query = f"""
            SELECT recovery_city,
                recovery_mother_name,
                recovery_birthday,
                recovery_setup
            FROM {self.user_table}
            WHERE email = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (email,))
                result = cur.fetchone()

            if not result:
                return "USER_NOT_FOUND"

            db_city, db_mother, db_bday, recovery_setup = result

            if not recovery_setup:
                return "RECOVERY_NOT_SETUP"

            # NORMALIZE (LOWERCASE + STRIP)
            city = city.strip().lower()
            mother_name = mother_name.strip().lower()

            db_city = (db_city or "").strip().lower()
            db_mother = (db_mother or "").strip().lower()

            # birthday compare (string safe)
            db_bday = str(db_bday)

            # CHECK ANSWERS
            if city != db_city or mother_name != db_mother or birthday != db_bday:

                self.rate_limit.check_rate_limit(
                    action="recovery_questions",
                    identifier=email,
                    max_attempts=5,
                    lock_minutes=5,
                )

                return "INVALID_ANSWERS"

            # SUCCESS → RESET LIMIT
            self.rate_limit.reset_rate_limit(
                "recovery_questions",
                email,
            )

            return "VERIFIED"

        except Exception as e:
            print("RECOVERY VERIFY ERROR:", e)
            return "ERROR"

    # RESET PASSWORD
    def reset_password(self, email, new_password):
        try:
            hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

            query = f"""
            UPDATE {self.user_table}
            SET password = %s,
                otp_code = NULL,
                otp_expires_at = NULL
            WHERE email = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (hashed, email))

            self.conn.commit()
            return "PASSWORD_RESET"

        except Exception as e:
            print("RESET PASSWORD ERROR:", e)
            return "ERROR"

    # LOGOUT USER
    def logout(self):
        try:
            if not self.current_user:
                return "NO_SESSION"

            # CLEAR SESSION ONLY
            self.current_user = None

            return "LOGOUT_SUCCESS"

        except Exception as error:
            print("LOGOUT ERROR:", error)
            return "ERROR"

    # FETCH LOGIN USER DIAGNOSTIC STATS
    def fetch_patient_diagnosis_stats(self, patient_id):
        try:
            query = f"""
            SELECT
                COUNT(*) AS total_tests,
                COUNT(pdf_path) AS total_reports,
                MAX(created_at) AS last_test_date,
                MAX(updated_at) AS last_activity
            FROM {self.diagnostic_table}
            WHERE patient_id = %s;
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (patient_id,))
                result = cur.fetchone()

            if not result:
                return None

            total_tests, total_reports, last_test_date, last_activity = result

            # FORMAT DATE → Apr 8
            formatted_date = (
                last_test_date.strftime("%b %d") if last_test_date else "N/A"
            )

            # TIME AGO FORMAT
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
                "total_tests": total_tests,
                "total_reports": total_reports,
                "last_test_date": formatted_date,
                "last_activity": time_ago(last_activity),
            }

        except Exception as error:
            print("FETCH DIAGNOSIS STATS ERROR:", error)
            return None

    # FETCH LINE CHART DATA
    def get_line_chart_data(self, patient_id):
        try:
            with self.conn.cursor() as cur:

                # ✅ TOTAL COUNT
                count_query = f"""
                SELECT COUNT(*)
                FROM {self.diagnostic_table}
                WHERE patient_id = %s;
                """
                cur.execute(count_query, (patient_id,))
                total_sessions = cur.fetchone()[0]

                # ✅ LAST 5 SESSIONS
                query = f"""
                SELECT
                    id,
                    temp,
                    test_confidence,
                    eye_confidence
                FROM {self.diagnostic_table}
                WHERE patient_id = %s
                ORDER BY created_at DESC
                LIMIT 5;
                """
                cur.execute(query, (patient_id,))
                rows = cur.fetchall()

            if not rows:
                return []

            # Reverse  oldest to newest
            rows.reverse()

            #  Compute starting session number
            start_session = max(1, total_sessions - len(rows) + 1)

            line_chart_data = []

            for i, row in enumerate(rows):
                _, temp, test_conf, eye_conf = row

                session_number = start_session + i

                line_chart_data.append(
                    {
                        "session": f"Session {session_number}",
                        "test": float(test_conf or 0),
                        "eye": float(eye_conf or 0),
                        "temp": float(temp or 0),
                    }
                )

            return line_chart_data

        except Exception as error:
            print("LINE CHART ERROR:", error)
            return []

    # FETCH BAR CHART DATA (risk_level)
    def get_bar_chart_data(self, patient_id):
        try:
            query = f"""
            SELECT
                eye_classification,
                COUNT(*) AS total
            FROM {self.diagnostic_table}
            WHERE patient_id = %s
            GROUP BY eye_classification;
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (patient_id,))
                rows = cur.fetchall()

            # ✅ Default categories (always shown)
            categories = {
                "Safe": 0,
                "Mild": 0,
                "Moderate": 0,
                "Severe": 0,
            }

            # Fill actual data
            for classification, count in rows:
                if classification in categories:
                    categories[classification] = count

            # Convert to UI format
            bar_chart_data = [
                {"classification": key, "value": value}
                for key, value in categories.items()
            ]

            return bar_chart_data

        except Exception as error:
            print("BAR CHART ERROR:", error)
            return []

    def fetch_patient_records(self, patient_id):
        try:
            query = f"""
            SELECT
                id,
                temp,
                test_classification,
                test_confidence,
                eye_classification,
                eye_confidence,
                risk_level,
                recommendation,
                created_at,
                answers,
                top_patient_factors,
                eye_image_path,
                eye_scan_path
            FROM {self.diagnostic_table}
            WHERE patient_id = %s
            ORDER BY created_at ASC;
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (patient_id,))
                rows = cur.fetchall()

            results = []

            for row in rows:
                (
                    diag_id,
                    temp,
                    test_class,
                    test_conf,
                    eye_class,
                    eye_conf,
                    risk,
                    recommendation,
                    created_at,
                    answers,
                    factors,
                    eye_img,
                    eye_scan,
                ) = row

                # ✅ safe conversions
                temp_display = f"{float(temp):.1f}°C" if temp is not None else "N/A"
                risk_display = str(risk) if risk else "N/A"

                results.append(
                    {
                        "id": diag_id,
                        "display": (
                            f"D{diag_id}",
                            temp_display,
                            test_class or "N/A",
                            eye_class or "N/A",
                            risk_display,
                        ),
                        "full": {
                            "id": diag_id,
                            "temp": temp,
                            "test_class": test_class,
                            "test_conf": test_conf,
                            "eye_class": eye_class,
                            "eye_conf": eye_conf,
                            "risk": risk,
                            "recommendation": recommendation,
                            "created_at": created_at,
                            "answers": answers or [],
                            "factors": factors or [],
                            "eye_image": eye_img,
                            "eye_scan": eye_scan,
                        },
                    }
                )

            return results or []  # ✅ never return None

        except Exception as error:
            print("FETCH RECORDS ERROR:", error)
            return []

    def search_patient_records(self, patient_id, keyword):
        try:
            query = f"""
            SELECT
                id,
                temp,
                test_classification,
                test_confidence,
                eye_classification,
                eye_confidence,
                risk_level,
                recommendation,
                created_at,
                answers,
                top_patient_factors,
                eye_image_path,
                eye_scan_path
            FROM {self.diagnostic_table}
            WHERE patient_id = %s
            AND (
                CAST(id AS TEXT) ILIKE %s OR
                CAST(temp AS TEXT) ILIKE %s OR
                test_classification ILIKE %s OR
                eye_classification ILIKE %s OR
                CAST(risk_level AS TEXT) ILIKE %s
            )
            ORDER BY created_at DESC;
            """

            search = f"%{keyword}%"

            with self.conn.cursor() as cur:
                cur.execute(query, (patient_id, search, search, search, search, search))
                rows = cur.fetchall()

            results = []

            for row in rows:
                (
                    diag_id,
                    temp,
                    test_class,
                    test_conf,
                    eye_class,
                    eye_conf,
                    risk,
                    recommendation,
                    created_at,
                    answers,
                    factors,
                    eye_img,
                    eye_scan,
                ) = row

                temp_display = f"{float(temp):.1f}°C" if temp is not None else "N/A"
                risk_display = str(risk) if risk else "N/A"

                results.append(
                    {
                        "id": diag_id,
                        "display": (
                            f"D{diag_id}",
                            temp_display,
                            test_class or "N/A",
                            eye_class or "N/A",
                            risk_display,
                        ),
                        "full": {
                            "id": diag_id,
                            "temp": temp,
                            "test_class": test_class,
                            "test_conf": test_conf,
                            "eye_class": eye_class,
                            "eye_conf": eye_conf,
                            "risk": risk,
                            "recommendation": recommendation,
                            "created_at": created_at,
                            "answers": answers or [],
                            "factors": factors or [],
                            "eye_image": eye_img,
                            "eye_scan": eye_scan,
                        },
                    }
                )

            return results or []

        except Exception as error:
            print("SEARCH ERROR:", error)
            return []

    def print_patient_results_table(self, diagnostic_id):
        try:
            query = f"""
            SELECT
                q.id,
                u.id,
                u.name,
                u.phone_number,
                q.temp,
                q.test_classification,
                q.test_confidence,
                q.eye_classification,
                q.eye_confidence,
                q.risk_level,
                q.recommendation,
                q.created_at
            FROM {self.diagnostic_table} q
            JOIN {self.user_table} u
            ON q.patient_id = u.id
            WHERE q.id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (diagnostic_id,))
                row = cur.fetchone()

            if not row:
                return None

            (
                result_id,
                patient_id,
                patient_name,
                phone_number,
                temp,
                test_class,
                test_conf,
                eye_class,
                eye_conf,
                risk,
                recommendation,
                created_at,
            ) = row

            return {
                "patient_id": f"P-{int(patient_id):03d}",
                "patient_name": patient_name,
                "contact_number": phone_number,
                "temperature": float(temp) if temp else 0,
                "test_result": test_class,
                "test_conf": test_conf,
                "eye_classification": eye_class,
                "eye_conf": round(float(eye_conf), 2) if eye_conf is not None else 0,
                "risk_level": risk,
                "recommendation": recommendation,
                "created_at": created_at,
            }

        except Exception as e:
            print("PRINT DATA ERROR:", e)
            return None

    # SAVE PATIENT TEMPERATURE
    def save_temperature(self, patient_id, temp):
        try:
            query = f"""
            INSERT INTO {self.diagnostic_table}
            (patient_id, temp)
            VALUES (%s, %s)
            RETURNING id
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (patient_id, temp))

                result = cur.fetchone()
                question_id = result[0] if result else None

            self.conn.commit()

            return question_id

        except Exception as error:
            print("SAVE TEMPERATURE ERROR:", error)
            return None

    # PASS THE TEMPERATURE
    def load_temperature(self, question_id):
        try:
            query = f"""
            SELECT temp
            FROM {self.diagnostic_table}
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (question_id,))
                result = cur.fetchone()

            return result[0] if result else None

        except Exception as error:
            print("LOAD TEMPERATURE ERROR:", error)
            return None

    def save_question_responses(
        self,
        question_id,
        answers,
        test_classification,
        test_confidence,
        top_patient_factors,
    ):
        try:
            factors_json = json.dumps(
                [{"feature": f, "score": float(s)} for f, s in top_patient_factors]
            )

            query = f"""
            UPDATE {self.diagnostic_table}
            SET
                answers = %s,
                test_classification = %s,
                test_confidence = %s,
                top_patient_factors = %s
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        answers,
                        test_classification,
                        float(test_confidence),
                        factors_json,
                        question_id,
                    ),
                )

            self.conn.commit()
            return True

        except Exception as error:
            print("SAVE QUESTION ERROR:", error)
            return False

    def load_test_results(self, question_id):
        try:
            query = f"""
            SELECT test_classification, test_confidence
            FROM {self.diagnostic_table}
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (question_id,))
                result = cur.fetchone()

            if result:
                return {
                    "classification": result[0],
                    "confidence": result[1],
                }

            return None

        except Exception as error:
            print("LOAD TEST RESULTS ERROR:", error)
            return None

    def save_eye_image(
        self,
        question_id,
        eye_image_path,
        eye_scan_path,
        eye_classification,
        eye_confidence,
    ):
        try:

            query = f"""
            UPDATE {self.diagnostic_table}
            SET eye_image_path = %s,
                eye_scan_path = %s,
                eye_classification = %s,
                eye_confidence = %s,
                updated_at = NOW()
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        eye_image_path,
                        eye_scan_path,
                        eye_classification,
                        eye_confidence,
                        question_id,
                    ),
                )

            self.conn.commit()
            return True

        except Exception as error:
            print("SAVE IMAGE ERROR:", error)
            return False

    def save_risk_and_recommendation(
        self,
        question_id,
        risk_level,
        recommendation,
    ):
        try:

            query = f"""
            UPDATE {self.diagnostic_table}
            SET risk_level = %s,
                recommendation = %s,
                updated_at = NOW()
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        risk_level,
                        recommendation,
                        question_id,
                    ),
                )

            self.conn.commit()
            return True

        except Exception as error:
            print("SAVE RISK ERROR:", error)
            return False

    def load_eye_results(self, question_id):
        try:
            query = f"""
            SELECT 
                eye_image_path,
                eye_scan_path,
                eye_classification,
                eye_confidence
            FROM {self.diagnostic_table}
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (question_id,))
                result = cur.fetchone()

            if result:
                return {
                    "eye_image": result[0],
                    "eye_scan": result[1],
                    "classification": result[2],
                    "confidence": result[3],
                }

            return None

        except Exception as error:
            print("LOAD EYE RESULTS ERROR:", error)
            return None

    def get_diagnosis_results(self, question_id):
        try:
            query = f"""
            SELECT temp, test_classification, test_confidence, top_patient_factors, eye_classification, eye_confidence, risk_level, recommendation
            FROM {self.diagnostic_table}
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (question_id,))
                row = cur.fetchone()

            if row:
                return {
                    "temp": row[0],
                    "test_classification": row[1],
                    "test_confidence": row[2],
                    "top_factors": row[3],
                    "eye_classification": row[4],
                    "eye_confidence": row[5],
                    "risk_level": row[6],
                    "recommendation": row[7],
                }

            return None

        except Exception as error:
            print("FETCH RESULT ERROR:", error)
            return None

    # GET RECEIPTS
    def get_receipt_data(self, question_id):
        try:
            query = f"""
            SELECT
                q.id,
                u.id,
                u.name,
                u.phone_number,
                q.temp,
                q.test_classification,
                q.test_confidence,
                q.eye_classification,
                q.eye_confidence,
                q.risk_level,
                q.recommendation,
                q.created_at
                
            FROM {self.diagnostic_table} q
            JOIN {self.user_table} u
            ON q.patient_id = u.id
            WHERE q.id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (question_id,))
                row = cur.fetchone()

            if not row:
                return None

            (
                result_id,
                patient_id,
                patient_name,
                phone_number,
                temp,
                test_classification,
                test_confidence,
                eye_classification,
                eye_confidence,
                risk_level,
                recommendation,
                created_at,
            ) = row

            date_str = created_at.strftime("%Y-%m-%d")
            time_str = created_at.strftime("%I:%M %p")

            return {
                "result_id": result_id,
                "patient_id": f"P-{int(patient_id):03d}",
                "patient_name": patient_name,
                "contact_number": phone_number,
                "temp": float(temp),
                "test_classification": test_classification,
                "test_confidence": test_confidence,
                "eye_classification": eye_classification,
                "eye_confidence": round(float(eye_confidence), 2),
                "risk_level": risk_level,
                "recommendation": recommendation,
                "date": date_str,
                "time": time_str,
            }

        except Exception as e:
            print("receipt data error:", e)
            return None

    # SAVE PDF
    def save_pdf_path(self, question_id, pdf_path):
        try:
            query = f"""
            UPDATE {self.diagnostic_table}
            SET pdf_path = %s,
                updated_at = NOW()
            WHERE id = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (pdf_path, question_id))

            self.conn.commit()
            return True

        except Exception as e:
            print("Save PDF Path Error:", e)
            return False

    # FETCH TOTAL USERS
    def fetch_users(self):
        pass

    # FETCH NEW USERS
    def fetch_new_users(self):
        pass

    # FETCH PATIENTS
    def fetch_patients(self):
        pass

    # FETCH TOTAL USERS
    def fetch_users(self):
        pass

    # FETCH NEW USERS
    def fetch_new_users(self):
        pass

    # FETCH PERSONNEL
    def fetch_personnel(self):
        pass

    # # EFFICIENT COUNTING FOR CARDS
    # def count_user_tests(self, patient_id):
    #     query = f"""
    #     SELECT COUNT(*)
    #     FROM {self.diagnostic_table}
    #     WHERE patient_id = %s
    #     """

    #     with self.conn.cursor() as cur:
    #         cur.execute(query, (patient_id,))
    #         return cur.fetchone()[0]

    # # ADMIN SIDE
    # def fetch_patients_and_personnel(self):
    #     try:
    #         query = f"""
    #         SELECT
    #             id,
    #             name,
    #             role
    #         FROM {self.user_table}
    #         WHERE role IN ('patient', 'personnel')
    #         ORDER BY created_at DESC
    #         """

    #         with self.conn.cursor() as cur:
    #             cur.execute(query)
    #             return cur.fetchall()

    #     except Exception as error:
    #         print(error)
    #         return []
    #     pass

    # # FETCH PATIENTS
    # def fetch_patients(self):
    #     try:
    #         query = f"""
    #         SELECT
    #             id,
    #             name,
    #             email
    #         FROM {self.user_table}
    #         WHERE role = 'patient'
    #         ORDER BY created_at DESC
    #         """

    #         with self.conn.cursor() as cur:
    #             cur.execute(query)
    #             return cur.fetchall()

    #     except Exception as error:
    #         print(error)
    #         return []

    # # FETCH PERSONNEL
    # def fetch_personnel(self):
    #     try:
    #         query = f"""
    #         SELECT
    #             id,
    #             name,
    #             email,
    #             DATE(created_at),
    #             DATE(updated_at)
    #         FROM {self.user_table}
    #         WHERE role = 'personnel'
    #         ORDER BY created_at DESC
    #         """

    #         with self.conn.cursor() as cur:
    #             cur.execute(query)
    #             return cur.fetchall()

    #     except Exception as error:
    #         print(error)
    #         return []

    # # SEARCH PATIENT
    # def search_patient(self, keyword):
    #     try:
    #         query = f"""
    #         SELECT id, name, email, created_at, updated_at
    #         FROM {self.user_table}
    #         WHERE role = 'patient'
    #         AND (
    #             name ILIKE %s
    #             OR email ILIKE %s
    #         )
    #         ORDER BY created_at DESC
    #         """

    #         search_term = f"%{keyword}%"

    #         with self.conn.cursor() as cur:
    #             cur.execute(query, (search_term, search_term))
    #             return cur.fetchall()

    #     except Exception as error:
    #         print(error)
    #         return []

    # # SEARCH PATIENT AND PERSONNEL
    # def search_patient_and_personnel(self, keyword):
    #     try:
    #         query = f"""
    #         SELECT id, name, role
    #         FROM {self.user_table}
    #         WHERE role IN ('patient', 'personnel')
    #         AND (
    #             name ILIKE %s
    #             OR role::text ILIKE %s
    #         )
    #         ORDER BY created_at DESC
    #         """

    #         term = f"%{keyword}%"

    #         with self.conn.cursor() as cur:
    #             cur.execute(query, (term, term))
    #             return cur.fetchall()

    #     except Exception as error:
    #         print(error)
    #         return []

    def close(self):
        self.cursor.close()
        self.conn.close()


# EX:
# db = DatabaseService()
# user = User(temp=0.01, answers=["Yes", "No"])

# db.save_response(user)
