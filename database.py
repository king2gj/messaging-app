import os
import mysql.connector
from mysql.connector import connect, Error

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

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