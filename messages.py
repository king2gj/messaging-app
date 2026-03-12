import uuid
import datetime

class standard_message:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not hasattr(self, "message_ID"):
            self.message_ID = uuid.uuid4()

        if not hasattr(self, "parent_ID"):
            self.parent_ID = None

        if not hasattr(self, "date_created"):
            self.date_created = datetime.datetime.now()

        if not hasattr(self, "message"):
            self.message = None

        if not hasattr(self, "creator_ID"):
            self.creator_ID = None

        if not hasattr(self, "likes"):
            self.likes = 0

        if not hasattr(self, "dislikes"):
            self.dislikes = 0

        if not hasattr(self, "report_count"):
            self.report_count = 0
            
        self.report_flag = False if self.report_count == 0 else True

       
        self.is_locked = True if self.report_count >= 3 else False

        
    def edit(self, new_message, user):
        if user == self.creator_ID or user.is_admin:
            self.message = new_message
        else:
            return "You cannot edit this message."

    def like(self):
        self.likes += 1

    def dislike(self):
        self.dislikes += 1

    def report(self, user):
        if user != self.creator_ID and not self.report_flag:
            if self.report_count < 3:
                self.message = "This message has been reported."
                self.likes = None
                self.dislikes = None
                self.creator_ID = None
                self.report_flag = True
                return "Message reported successfully. Message has been taken down for review."
            else:
                self.report_count += 1
                return "Message reported successfully."
        else:
            return "You cannot report your own message."

    def __str__(self):
        if self.is_locked:
            return "This message has been locked."
        else:
            return f"{self.message} - {self.creator_ID} ({self.likes} likes, {self.dislikes} dislikes)"
    
class announcement:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not hasattr(self, "message_ID"):
            self.message_ID = uuid.uuid4()

        if not hasattr(self, "parent_ID"):
            self.parent_ID = None

        if not hasattr(self, "date_created"):
            self.date_created = datetime.datetime.now()

        if not hasattr(self, "message"):
            self.message = None

        if not hasattr(self, "creator_ID"):
            self.creator_ID = None

        if not hasattr(self, "likes"):
            self.likes = 0

        if not hasattr(self, "dislikes"):
            self.dislikes = 0

        if not hasattr(self, "report_count"):
            self.report_count = 0
            
        self.report_flag = False if self.report_count == 0 else True

       
        self.is_locked = True if self.report_count >= 3 else False


    def edit(self, new_message, user):
        if user == self.creator or user.is_admin:
            self.message = new_message
        else:
            return "You cannot edit this announcement."
    
    def report(self, user):
        if user != self.creator and not self.report_flag:
            if self.report_count < 3:
                self.message = "This announcement has been reported."
                self.creator = None
                self.report_flag = True
                return "Announcement reported successfully. Announcement has been taken down for review."
            else:
                self.report_count += 1
                return "Announcement reported successfully."
        else:
            return "You cannot report your own announcement."

    def __str__(self):
        if self.is_locked:
            return "This announcement has been locked."
        else:
            return f"{self.message} - {self.creator_ID}"

class message_factory:
    @staticmethod
    def create_message(message_type, message, creator_ID, parent_ID):
        if message_type == "standard":
            return standard_message(message, creator_ID, parent_ID)
        elif message_type == "announcement":
            return announcement(message, creator_ID, parent_ID)
        else:
            raise ValueError("Invalid message type")