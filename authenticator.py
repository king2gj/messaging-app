import json
import hashlib
import database


class Authenticator:

    db = database.access_database()
    conn = db.connect()

    def __init__(self):
        self.salt = "random_salt"
        self.user_data = None

    def hash_password(self, password):
        salted_password = password + self.salt
        hashed_password = hashlib.sha256(salted_password.encode()).digest()
        return hashed_password
    
    def save_user_data(self, email, username, password, conn_cursor):
        hashed_password = self.hash_password(password)
        if self.db.newuser(email, username, hashed_password, conn_cursor):
            return True
        else:
            return False
        
    def load_user_data(self, username):
        try:
            return self.db.getuser(username, self.conn.cursor())
        except FileNotFoundError:
            return {}


    def authenticate(self, username, password):
        user_data = self.load_user_data(username)
        salted_password = password + self.salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        goodauth = self.db.user_login(username, hashed_password, self.conn.cursor())
        if goodauth:
            return True
        else:      
            return False
        