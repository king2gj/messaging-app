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

def get_user_id(
        username: str,
        cursor) -> bytes:
    sql = load_sql("sql/users/get_id_by_username.sql")
    params = (username,)
    cursor.execute(sql, params)

    (user_id,) = cursor.fetchone()
    return user_id

def add_new_user(
        user_id: bytes,
        username: str,
        first_name: str,
        last_name: str,
        email:str,
        bio: str,
        is_admin: bool,
        hashed_password: bytes,
        salt_code: str,
        cursor) -> None:
    if len(user_id) != 16:
        raise ValueError("ID must be 16 bytes")
    for x in {username, first_name, last_name, email}:
        if len(x) > 32:
            raise ValueError("Username, first name, last name, and email cannot exceed 32 characters")
    if len(bio) > 160:
        raise ValueError("Bio cannot exceed 160 characters")
    if len(hashed_password) != 32:
        raise ValueError("Hashed password must be 32 bytes")
    if len(salt_code) > 32:
        raise ValueError("Salt code cannot exceed 32 characters")

    sql = load_sql("sql/users/create_new_user.sql")
    params = (user_id, username, first_name, last_name, email, bio, is_admin)
    cursor.execute(sql, params)

    sql = load_sql("sql/auth/create_new_auth.sql")
    params = (user_id, hashed_password, salt_code)
    cursor.execute(sql, params)

def add_new_report(
        report_id: bytes,
        reporter_id: bytes,
        post_id: bytes,
        report_content: str,
        cursor) -> None:
    for x in {report_id, reporter_id, post_id}:
        if len(x) != 16:
            raise ValueError("All IDs must be 16 bytes")
    if len(report_content) > 200:
        raise ValueError("Report content cannot exceed 200 characters")

    sql = load_sql("sql/reports/create_new_report.sql")
    params = (report_id, reporter_id, post_id, report_content)
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