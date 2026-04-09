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
            usercheck = database.get_user_id_by_email(email)
            print(f"usercheck result: {usercheck}")
            if usercheck is not None:
                return "exists"
            self.salt = uuid.uuid4().hex
            hashed_password = self.hash_password(password)
            result = database.add_new_user(username=username, email=email, bio="", is_admin=False, hashed_password=hashed_password, salt_code=self.salt)
            return "success"
        except Exception as e:
            print(f"Error saving user data: {e}")
            return "error"
    def load_user_data(self, username):
        try:
            return self.db.getuser(username)
        except FileNotFoundError:
            return {}


    def authenticate(self, email, password):
        try:
            user_id = database.get_user_id_by_email(email)
            if user_id is None:
                return False
            hashed_password, salt_code = database.get_user_auth_info_by_id(user_id)
            self.salt = salt_code  # load the real salt from DB
            test_hash = self.hash_password(password)  # uses .digest() consistently
            if test_hash == bytes(hashed_password):  # ensure both are bytes
                return True
            return False
        except Exception as e:
            print(f"Auth error: {e}")
            return False
        