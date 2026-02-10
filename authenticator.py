import json
import hashlib

class Authenticator:
    def __init__(self):
        self.salt = "random_salt"
        self.user_data = None

    def hash_password(self, password):
        salted_password = password + self.salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashed_password
    
    def save_user_data(self, username, password):
        hashed_password = self.hash_password(password)
        dump_obj = {username: hashed_password}
        try:
            user_data = self.load_user_data()
            user_data.update(dump_obj)
            with open('user_auth.json', 'w') as file:
                json.dump(user_data, file, indent = 4)
        except FileNotFoundError:
            with open('user_auth.json', 'w') as file:
                json.dump(dump_obj, file, indent = 4)
        
    def load_user_data(self):
        with open('user_auth.json', 'r') as file:
            user_data = json.load(file)
        return user_data

    def authenticate(self, username, password):
        user_data = self.load_user_data()
        salted_password = password + self.salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        if username in user_data and user_data[username] == hashed_password:
            return True
        else:
            return False
