import datetime
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass
from mysql.connector import connect, Error

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
class standard_user:
    def __init__(self, email, password):
        self.name = email
        self.type = "standard_user"
        self.is_admin = False
        self.date_joined = datetime.datetime.now()
        self.last_online = None
        self.online = False
        self.posts = []
        self.post_count = 0
        self.bio = None
        self.profile_picture = None # change to a path to a file later
        # below 2 attributes will be changed to accessing an authentication system. probably a json containing hashed values for now.
        self.username = email
        self.password = password
        self.auth_success = False


    def login(self, authenticator):
        if authenticator and self.online == False:
            self.online = True
            self.last_online = datetime.datetime.now()
            self.auth_success = True
            return f"{self.name} has logged in."
        elif authenticator and self.online == True:
            self.auth_success = False
            return f"{self.name} is already logged in."
        else:
            self.auth_success = False
            return "Invalid email or password."

    def logout(self):
        self.online = False
        self.last_online = datetime.datetime.now()
        return f"{self.name} has logged out."

    def get_profile(self):
        return f"Name: {self.name}\nType: {self.type}\nDate Joined: {self.date_joined}\nOnline: {self.online}\nLast Online: {self.last_online}\nBio: {self.bio}\nPosts: {self.post_count}"

    def report_user(self):
        pass
        # this will be changed to accessing a reporting system. probably a json containing reported users for now.

    def delete_account(self):
        pass
        # this will be changed to accessing a deletion system. probably a json containing deleted users for now.

    def edit_profile(self, name, bio, profile_picture):
        self.name = name
        self.bio = bio
        self.profile_picture = profile_picture
        return f"Profile updated."

class admin_user(standard_user):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.type = "admin_user"
        self.is_admin = True
        self.posts = []
        self.post_count = 0
        self.bio = None
        self.profile_picture = None # change to a path to a file later
        self.email = email
        self.password = password
        self.auth_success = False
    

    def delete_user(self, user):
        pass
        # this will be changed to accessing a deletion system.

    def ban_user(self, user):
        pass
        # this will be changed to accessing a banning system. 

    def unban_user(self, user):
        pass
        # this will be changed to accessing a banning system. 

    def delete_post(self, post):
        pass
        # this will be changed to accessing a deletion system. 
 
