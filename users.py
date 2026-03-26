import datetime
import uuid

class StandardUser:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        if not hasattr(self, 'user_ID'):
            self.user_ID = uuid.uuid4()

        if not hasattr(self, 'username'):
            self.username = None

        self.type = "standard_user"
        self.is_admin = False

        if not hasattr(self, 'date_joined'):
            self.date_joined = datetime.datetime.now()

        if not hasattr(self, 'last_online'):
            self.last_online = datetime.datetime.now()

        if not hasattr(self, 'online'):
            self.online = True

        if not hasattr(self, 'posts'):
            self.posts = []

        if not hasattr(self, 'post_count'):
            self.post_count = 0

        if not hasattr(self, 'bio'):
            self.bio = None

        if not hasattr(self, 'profile_picture'):
            self.profile_picture = None
        
        if not hasattr(self, "email"):
            self.email = None
        
        if not hasattr(self, "password"):
            self.password = None

        if not hasattr(self, 'auth_success'):
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

    def edit_profile(self, name = None, bio = None, profile_picture = None):
        self.name = name
        self.bio = bio
        self.profile_picture = profile_picture
        return f"Profile updated."

class AdminUser:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        if not hasattr(self, 'user_ID'):
            self.user_ID = uuid.uuid4()

        if not hasattr(self, 'username'):
            self.username = None

        self.type = "admin_user"
        self.is_admin = True

        if not hasattr(self, 'date_joined'):
            self.date_joined = datetime.datetime.now()

        if not hasattr(self, 'last_online'):
            self.last_online = datetime.datetime.now()

        if not hasattr(self, 'online'):
            self.online = True

        if not hasattr(self, 'posts'):
            self.posts = []

        if not hasattr(self, 'post_count'):
            self.post_count = 0

        if not hasattr(self, 'bio'):
            self.bio = None

        if not hasattr(self, 'profile_picture'):
            self.profile_picture = None
        
        if not hasattr(self, "email"):
            self.email = None
        
        if not hasattr(self, "password"):
            self.password = None

        if not hasattr(self, 'auth_success'):
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

    def edit_profile(self, name = None, bio = None, profile_picture = None):
        self.name = name
        self.bio = bio
        self.profile_picture = profile_picture
        return f"Profile updated."
