from datetime import datetime, timedelta, timezone
from .config.connect_db import connect_db


class RateLimitService:
    def __init__(self):
        self.rate_limit_table = "rate_limits"
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def check_rate_limit(self, action, identifier, max_attempts, lock_minutes):
        try:
            query = """
            SELECT attempts, locked_until
            FROM rate_limits
            WHERE action = %s AND identifier = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(query, (action, identifier))
                row = cur.fetchone()

            now = datetime.now(timezone.utc)

            # FIRST ATTEMPT
            if not row:
                insert = """
                INSERT INTO rate_limits (action, identifier, attempts)
                VALUES (%s, %s, 1)
                """
                with self.conn.cursor() as cur:
                    cur.execute(insert, (action, identifier))
                self.conn.commit()

                return {"allowed": True}

            attempts, locked_until = row

            # STILL LOCKED
            if locked_until and locked_until > now:
                remaining = int((locked_until - now).total_seconds())
                return {
                    "allowed": False,
                    "remaining_seconds": remaining,
                }

            # INCREMENT ATTEMPTS
            attempts += 1

            lock_time = None
            if attempts >= max_attempts:
                lock_time = now + timedelta(minutes=lock_minutes)

            update = """
            UPDATE rate_limits
            SET attempts = %s,
                locked_until = %s,
                updated_at = NOW()
            WHERE action = %s AND identifier = %s
            """

            with self.conn.cursor() as cur:
                cur.execute(update, (attempts, lock_time, action, identifier))

            self.conn.commit()

            return {"allowed": True}

        except Exception as e:
            print(e)
            return {"allowed": False}

    def is_locked(self, action, identifier):
        query = """
        SELECT locked_until
        FROM rate_limits
        WHERE action = %s AND identifier = %s
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (action, identifier))
            row = cur.fetchone()

        if not row:
            return {"locked": False}

        locked_until = row[0]

        if locked_until and locked_until > datetime.now(timezone.utc):
            remaining = int((locked_until - datetime.now(timezone.utc)).total_seconds())
            return {"locked": True, "remaining": remaining}

        return {"locked": False}

    def reset_rate_limit(self, action, identifier):
        query = """
        UPDATE rate_limits
        SET attempts = 0,
            locked_until = NULL,
            updated_at = NOW()
        WHERE action = %s AND identifier = %s
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (action, identifier))

        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
