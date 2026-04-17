# # FETCH PATIENT RECORDS BASED ON LOGIN PATIENT
# def fetch_patient_records(self, patient_id):
#     try:
#         query = f"""
#         SELECT
#             id,
#             temp,
#             test_classification,
#             eye_classification,
#             risk_level
#         FROM {self.diagnostic_table}
#         WHERE patient_id = %s
#         ORDER BY created_at ASC;
#         """

#         with self.conn.cursor() as cur:
#             cur.execute(query, (patient_id,))
#             rows = cur.fetchall()

#         if not rows:
#             return []

#         table_data = []

#         for row in rows:
#             diag_id, temp, test_class, eye_class, risk = row

#             table_data.append(
#                 (
#                     f"D{diag_id}",
#                     f"{float(temp):.1f}°C" if temp else "N/A",
#                     test_class or "N/A",
#                     eye_class or "N/A",
#                     f"{float(risk):.2f}" if risk else "N/A",
#                 )
#             )

#         return table_data

#     except Exception as error:
#         print("FETCH RECORDS ERROR:", error)
#         return []

# def fetch_patient_records(self, patient_id):
#     try:
#         query = f"""
#         SELECT
#             id,
#             temp,
#             test_classification,
#             test_confidence,
#             eye_classification,
#             eye_confidence,
#             risk_level,
#             recommendation,
#             created_at,
#             answers,
#             top_patient_factors,
#             eye_image_path,
#             eye_scan_path
#         FROM {self.diagnostic_table}
#         WHERE patient_id = %s
#         ORDER BY created_at ASC;
#         """

#         with self.conn.cursor() as cur:
#             cur.execute(query, (patient_id,))
#             rows = cur.fetchall()

#         results = []

#         for row in rows:
#             (
#                 diag_id,
#                 temp,
#                 test_class,
#                 test_conf,
#                 eye_class,
#                 eye_conf,
#                 risk,
#                 recommendation,
#                 created_at,
#                 answers,
#                 factors,
#                 eye_img,
#                 eye_scan,
#             ) = row

#             results.append(
#                 {
#                     "id": diag_id,
#                     "display": (
#                         f"D{diag_id}",
#                         f"{float(temp):.1f}°C" if temp else "N/A",
#                         test_class or "N/A",
#                         eye_class or "N/A",
#                         f"{float(risk):.2f}" if risk else "N/A",
#                     ),
#                     "full": {
#                         "id": diag_id,
#                         "temp": temp,
#                         "test_class": test_class,
#                         "test_conf": test_conf,
#                         "eye_class": eye_class,
#                         "eye_conf": eye_conf,
#                         "risk": risk,
#                         "recommendation": recommendation,
#                         "created_at": created_at,
#                         "answers": answers,
#                         "factors": factors,
#                         "eye_image": eye_img,
#                         "eye_scan": eye_scan,
#                     },
#                 }
#             )

#         return results

#     except Exception as error:
#         print("FETCH RECORDS ERROR:", error)
#         return []

# # SEARCH PATIENT RECORD BASED ON LOGIN PATIENT
# def search_patient_records(self, patient_id, keyword):
#     try:
#         query = f"""
#         SELECT
#             id,
#             temp,
#             test_classification,
#             eye_classification,
#             risk_level
#         FROM {self.diagnostic_table}
#         WHERE patient_id = %s
#         AND (
#             CAST(id AS TEXT) ILIKE %s OR
#             CAST(temp AS TEXT) ILIKE %s OR
#             test_classification ILIKE %s OR
#             eye_classification ILIKE %s OR
#             CAST(risk_level AS TEXT) ILIKE %s
#         )
#         ORDER BY created_at DESC;
#         """

#         search = f"%{keyword}%"

#         with self.conn.cursor() as cur:
#             cur.execute(query, (patient_id, search, search, search, search, search))
#             rows = cur.fetchall()

#         table_data = []

#         for row in rows:
#             diag_id, temp, test_class, eye_class, risk = row

#             table_data.append(
#                 (
#                     f"D{diag_id}",
#                     f"{float(temp):.1f}°C" if temp else "N/A",
#                     test_class or "N/A",
#                     eye_class or "N/A",
#                     f"{float(risk):.2f}" if risk else "N/A",
#                 )
#             )

#         return table_data

#     except Exception as error:
#         print("SEARCH ERROR:", error)
#         return []


# def handle_search(self):
#     user = self.controller.current_user

#     if not user:
#         return

#     user_id = user[0]
#     keyword = self.search_entry.get().strip()

#     # If empty → show all records again
#     if not keyword:
#         data = self.controller.db.fetch_patient_records(user_id)
#     else:
#         data = self.controller.db.search_patient_records(user_id, keyword)

#     if not data:
#         data = [("No Results", "-", "-", "-", "-")]

#     self.table.update_data(data)

# def on_show(self):
#     user = self.controller.current_user

#     if not user:
#         return

#     user_id = user[0]
#     records = self.controller.db.fetch_patient_records(user_id)

#     self.full_records = records
#     self.table_data = [r["display"] for r in records]

#     if not self.table_data:
#         self.table_data = [("No Data", "-", "-", "-", "-")]

#     self.table.update_data(self.table_data)
#     self.search_entry.configure(placeholder_text="Search records...")
