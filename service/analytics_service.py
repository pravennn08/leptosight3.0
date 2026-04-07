from .config.connect_db import connect_db


class AnalyticService:
    def __init__(self):
        self.conn = connect_db()
        self.user_table = "users"
        self.question_table = "questions"

    def line_chart_data(self):
        query = f"""
        SELECT
            DATE(created_at) AS day,
            COUNT(*) FILTER (WHERE role = 'patient') AS patients,
            COUNT(*) FILTER (WHERE role = 'personnel') AS personnel
        FROM {self.user_table}
        GROUP BY day
        ORDER BY day
        """

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        if not rows:
            return [], [], []

        days = [str(r[0]) for r in rows]
        patients = [r[1] for r in rows]
        personnel = [r[2] for r in rows]

        return days, patients, personnel

    def bar_chart_data(self):
        query = f"""
        SELECT role, COUNT(*)
        FROM {self.user_table}
        WHERE role IN ('patient', 'personnel')
        GROUP BY role
        """

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        counts = {role: count for role, count in rows}

        return ["Patients", "Personnel"], [
            counts.get("patient", 0),
            counts.get("personnel", 0),
        ]
