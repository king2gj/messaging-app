import datetime

"""
Valid Console Reasons:
1. Reported object moderation
2. User moderation
3. Object/user adjustments/edits
4. Other valid reasons (select other and then text entry) Save reasons as string for DB.

"""

class AdminConsole:
    def __init__(self, admin_user, focus_object, reason):
        if admin_user.is_admin:
            self.admin_user = admin_user
            self.focus_object = focus_object
            self.reason = reason
            self.created_at = datetime.datetime.now()
        else:
            raise ValueError("User is not an admin.")
            

    def unlock_object(self):
        self.focus_object.is_locked = False

    def lock_object(self):
        self.focus_object.is_locked = True

    def reset_reports(self):
        self.focus_object.report_count = 0
        self.focus_object.is_reported = False

    def get_object_type(self):
        return type(self.focus_object)
    
    def view_object_data(self):
        return vars(self.focus_object)
    
    def set_object_attribute(self, name, value):
        try:
            setattr(self.focus_object, name, value)
        except:
            raise AttributeError(f"{name} is not a valid attribute in {self.focus_object}")

    def call_object_method(self, name, *args, **kwargs):
        method = getattr(self.focus_object, name)
        if callable(method):
            return method(*args, **kwargs)
        else:
            raise AttributeError(f"{name} is not a valid method in {self.focus_object}")
    

            
    