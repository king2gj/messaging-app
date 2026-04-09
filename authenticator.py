import json
import hashlib
import uuid
import database


class Authenticator:

    db = database.access_database()
    conn = db.connect()

    def __init__(self):
        self.salt = "None"
        self.user_data = None

    def hash_password(self, password):
        salted_password = password + self.salt
        hashed_password = hashlib.sha256(salted_password.encode()).digest()
        return hashed_password
    
    def save_user_data(self, email, username, password):
        try:
        self.salt = uuid.uuid4().hex
        hashed_password = self.hash_password(password)
        result = database.add_new_user(username=username, email=email, bio="", is_admin=False, hashed_password=hashed_password, salt_code=self.salt, cursor=self.conn.cursor()):
        return result
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
        