import uuid
import datetime

class standard_message:
    def __init__(self, **kwargs):
        if "message_ID" in kwargs:
            self.message_ID = kwargs["message_ID"]
        else:
            self.message_ID = uuid.uuid4()
        
        if "parent_ID" in kwargs:
            self.parent_ID = kwargs["parent_ID"]
        else:
            self.parent_ID = None

        if "date_created" in kwargs:
            self.date_created = kwargs["date_created"]
        else:
            self.date_created = datetime.datetime.now()

        if "message" in kwargs:
            self.message = kwargs["message"]
        else:
            self.message = None

        if "creator_ID" in kwargs:
            self.creator_ID = kwargs["creator_ID"]
        else:
            self.creator_ID = None

        if "likes" in kwargs:
            self.likes = kwargs["likes"]
        else:
            self.likes = 0

        if "dislikes" in kwargs:
            self.dislikes = kwargs["dislikes"]
        else:
            self.dislikes = 0

        if "report_count" in kwargs:
            self.report_count = kwargs["report_count"]
            self.report_flag = True
        else:
            self.report_count = 0
            self.report_flag = False

        if "is_locked" in kwargs:
            self.is_locked = kwargs["is_locked"]
        else:
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
        if "message_ID" in kwargs:
            self.message_ID = kwargs["message_ID"]
        else:
            self.message_ID = uuid.uuid4()
        
        if "parent_ID" in kwargs:
            self.parent_ID = kwargs["parent_ID"]
        else:
            self.parent_ID = None

        if "date_created" in kwargs:
            self.date_created = kwargs["date_created"]
        else:
            self.date_created = datetime.datetime.now()

        if "message" in kwargs:
            self.message = kwargs["message"]
        else:
            self.message = None

        if "creator_ID" in kwargs:
            self.creator_ID = kwargs["creator_ID"]
        else:
            self.creator_ID = None

        if "report_count" in kwargs:
            self.report_count = kwargs["report_count"]
            self.report_flag = True if self.report_count > 0 else False
        else:
            self.report_count = 0
            self.report_flag = False

        if "is_locked" in kwargs:
            self.is_locked = kwargs["is_locked"]
        else:
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
    def create_message(message_type, message, creator_ID, thread_ID):
        if message_type == "standard":
            return standard_message(message, creator_ID, thread_ID)
        elif message_type == "announcement":
            return announcement(message, creator_ID, thread_ID)
        else:
            raise ValueError("Invalid message type")

