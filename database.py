import os
import mysql.connector
from mysql.connector import connect, Error
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def load_sql(path: str | Path) -> str:
    path = Path(path)
    return path.read_text(encoding="utf-8")

def add_new_report(reporter_id: int, post_id: int, report_content: str, cursor):
    if len(report_content) > 200:
        raise ValueError("Report content cannot exceed 200 characters")

    sql = load_sql("sql/reports/create_new_report.sql")
    params = (reporter_id, post_id, report_content)
    cursor.execute(sql, params)

    sql = load_sql("sql/posts/increment_report_count.sql")
    params = (post_id,)
    cursor.execute(sql, params)

class access_database:
    def __init__(self, host=None, user=None, password=None, database=None, port=None):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.user = user or os.getenv("DB_USER", "python")
        self.password = password or os.getenv("DB_PASS", "python")
        self.database = database or os.getenv("DB_NAME", "auth")
        self.port = int(port or os.getenv("DB_PORT", 3306))

    def connect(self):
        try:
            conn = connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.database,
            )
            with conn.cursor() as cur:
                cur.execute("SELECT DATABASE();")
                db = cur.fetchone()
                cur.execute("SELECT * FROM user WHERE fname = %s;", ("Liberty",))
                user = cur.fetchone()
                print(f"Connected to database: {db}")
                print(f"User fetched: {user}")

            return conn
        except Error as e:
            print(e)
            return None


if __name__ == "__main__":
    # quick runtime check when executing this file directly
    db = access_database()
    conn = db.connect()
    if conn:
        print("Connection established.")
        try:
            conn.close()
        except Exception:
            pass
    else:
        print("Failed to connect to database.")