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

def user_login(email: str, password: str, cursor) -> bool:
    sql = load_sql("sql/authentication/user_login.sql")
    params = (email, password)
    cursor.execute(sql, params)
    result = cursor.fetchone()
    return result is not None

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

            return conn
        except Error as e:
            print(e)
            return None
        
    def getuser(self, email: str, cursor):
        sql = load_sql("sql/authentication/get_user.sql")
        params = (email)
        cursor.execute(sql, params)
        result = cursor.fetchone()
        return result #this returned result should be the user object
    def newuser(self, email: str, password: str, username: str):
        try:
            conn = self.connect()
            if conn is None:
                print("Failed to connect to database.")
                return False
            with conn.cursor() as cur:
                sql = load_sql("sql/authentication/create_new_user.sql")
                params = (email, password)
                cur.execute(sql, params)
                conn.commit()
    
            return True
        except Error as e:
            print(e)
            return False
    def updateuser(self, email: str, password: str):
        try:
            conn = self.connect()
            if conn is None:
                print("Failed to connect to database.")
                return False
            with conn.cursor() as cur:
                sql = load_sql("sql/authentication/update_user.sql")
                params = (email, password, )
                cur.execute(sql, params)
                conn.commit()
    
            return True
        except Error as e:
            print(e)
            return False
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