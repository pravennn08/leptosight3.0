# def handle_search(self):
#     if hasattr(self, "search_after_id"):
#         self.after_cancel(self.search_after_id)

#     self.search_after_id = self.after(300, self.smooth_search)

# def smooth_search(self):
#     keyword = self.search_entry.get().strip()

#     if not keyword:
#         records = self.admin_db.fetch_all_users()
#     else:
#         records = self.admin_db.search_user(keyword)

#     records = records or []
#     self.full_records = records

#     if records:
#         table_data = [r.get("display", ("-", "-", "-", "-", "-")) for r in records]
#     else:
#         table_data = [("No Results", "-", "-", "-", "-")]

#     self.table.update_data(table_data)

# def handle_role_filter(self, selected_role):
#     records = self.admin_db.filter_user_role(selected_role)

#     records = records or []
#     self.full_records = records

#     if records:
#         table_data = [r.get("display", ("-", "-", "-", "-", "-")) for r in records]
#     else:
#         table_data = [("No Results", "-", "-", "-", "-", "-")]

#     self.table.update_data(table_data)

# def handle_status_filter(self, selected_status):
#     records = self.admin_db.filter_user_status(selected_status)

#     records = records or []
#     self.full_records = records

#     if records:
#         table_data = [r.get("display", ("-", "-", "-", "-", "-")) for r in records]
#     else:
#         table_data = [("No Results", "-", "-", "-", "-", "-")]

#     self.table.update_data(table_data)

# service


# def search_user(self, keyword):
#     try:
#         with self.conn.cursor() as cur:

#             query = f"""
#             SELECT
#                 id,
#                 name,
#                 email,
#                 phone_number,
#                 password,
#                 role,
#                 is_verified,
#                 last_login_at,
#                 created_at,
#                 updated_at
#             FROM {self.user_table}
#             WHERE
#                 id::text ILIKE %s OR
#                 name ILIKE %s OR
#                 email ILIKE %s OR
#                 phone_number ILIKE %s OR
#                 role::text ILIKE %s OR
#                 (
#                     CASE
#                         WHEN is_verified = TRUE THEN 'verified'
#                         ELSE 'pending'
#                     END
#                 ) ILIKE %s
#             ORDER BY created_at DESC
#             """

#             like_keyword = f"%{keyword}%"

#             cur.execute(
#                 query,
#                 (
#                     like_keyword,
#                     like_keyword,
#                     like_keyword,
#                     like_keyword,
#                     like_keyword,
#                     like_keyword,
#                 ),
#             )

#             rows = cur.fetchall()

#         if not rows:
#             return []

#         results = []

#         for row in rows:
#             (
#                 user_id,
#                 name,
#                 email,
#                 phone,
#                 password,
#                 role,
#                 is_verified,
#                 last_login,
#                 created_at,
#                 updated_at,
#             ) = row

#             role_text = role.capitalize() if role else "N/A"

#             # ✅ FIXED STATUS
#             status = "Verified" if bool(is_verified) else "Pending"

#             display = (
#                 user_id,  # ✅ no formatting
#                 email,
#                 phone,
#                 role_text,
#                 status,
#                 "View",
#             )

#             full = {
#                 "id": user_id,
#                 "name": name,
#                 "email": email,
#                 "phone_number": phone,
#                 "password": password,
#                 "role": role,
#                 "is_verified": is_verified,
#                 "last_login_at": last_login,
#                 "created_at": created_at,
#                 "updated_at": updated_at,
#             }

#             results.append(
#                 {
#                     "id": user_id,
#                     "display": display,
#                     "full": full,
#                 }
#             )

#         return results

#     except Exception as error:
#         self.conn.rollback()
#         print("SEARCH USER ERROR:", error)
#         return None

# def filter_user_role(self, role):
#     try:
#         with self.conn.cursor() as cur:

#             # ✅ If ALL → return everything
#             if role.lower() == "all":
#                 return self.fetch_all_users()

#             query = f"""
#             SELECT
#                 id,
#                 name,
#                 email,
#                 phone_number,
#                 password,
#                 role,
#                 is_verified,
#                 last_login_at,
#                 created_at,
#                 updated_at
#             FROM {self.user_table}
#             WHERE role::text = %s
#             ORDER BY created_at DESC
#             """

#             cur.execute(query, (role.lower(),))
#             rows = cur.fetchall()

#         if not rows:
#             return []

#         results = []

#         for row in rows:
#             (
#                 user_id,
#                 name,
#                 email,
#                 phone,
#                 password,
#                 role,
#                 is_verified,
#                 last_login,
#                 created_at,
#                 updated_at,
#             ) = row

#             role_text = role.capitalize() if role else "N/A"
#             status = "Verified" if bool(is_verified) else "Pending"

#             display = (
#                 user_id,
#                 email,
#                 phone,
#                 role_text,
#                 status,
#                 "View",
#             )

#             full = {
#                 "id": user_id,
#                 "name": name,
#                 "email": email,
#                 "phone_number": phone,
#                 "password": password,
#                 "role": role,
#                 "is_verified": is_verified,
#                 "last_login_at": last_login,
#                 "created_at": created_at,
#                 "updated_at": updated_at,
#             }

#             results.append(
#                 {
#                     "id": user_id,
#                     "display": display,
#                     "full": full,
#                 }
#             )

#         return results

#     except Exception as error:
#         self.conn.rollback()
#         print("FILTER ROLE ERROR:", error)
#         return None

# def filter_user_status(self, status):
#     try:
#         with self.conn.cursor() as cur:

#             # ✅ ALL → return everything
#             if status.lower() == "all":
#                 return self.fetch_all_users()

#             # ✅ Convert UI → boolean
#             is_verified = True if status.lower() == "verified" else False

#             query = f"""
#             SELECT
#                 id,
#                 name,
#                 email,
#                 phone_number,
#                 password,
#                 role,
#                 is_verified,
#                 last_login_at,
#                 created_at,
#                 updated_at
#             FROM {self.user_table}
#             WHERE is_verified = %s
#             ORDER BY created_at DESC
#             """

#             cur.execute(query, (is_verified,))
#             rows = cur.fetchall()

#         if not rows:
#             return []

#         results = []

#         for row in rows:
#             (
#                 user_id,
#                 name,
#                 email,
#                 phone,
#                 password,
#                 role,
#                 is_verified,
#                 last_login,
#                 created_at,
#                 updated_at,
#             ) = row

#             role_text = role.capitalize() if role else "N/A"
#             status_text = "Verified" if bool(is_verified) else "Pending"

#             display = (
#                 user_id,
#                 email,
#                 phone,
#                 role_text,
#                 status_text,
#                 "View",
#             )

#             full = {
#                 "id": user_id,
#                 "name": name,
#                 "email": email,
#                 "phone_number": phone,
#                 "password": password,
#                 "role": role,
#                 "is_verified": is_verified,
#                 "last_login_at": last_login,
#                 "created_at": created_at,
#                 "updated_at": updated_at,
#             }

#             results.append(
#                 {
#                     "id": user_id,
#                     "display": display,
#                     "full": full,
#                 }
#             )

#         return results

#     except Exception as error:
#         self.conn.rollback()
#         print("FILTER STATUS ERROR:", error)
#         return None
