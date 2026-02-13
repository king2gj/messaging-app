class standard_message:
    def __init__(self, message, creator):
        self.message = message
        self.creator = creator
        self.likes = 0
        self.dislikes = 0
        self.priority = 0
        self.report_count = 0
        self.report_flag = False

    def edit(self, new_message, user):
        if user == self.creator or user.is_admin:
            self.message = new_message
        else:
            return "You cannot edit this message."

    def like(self):
        self.likes += 1

    def dislike(self):
        self.dislikes += 1

    def report(self, user):
        if user != self.creator and not self.report_flag:
            if self.report_count < 3:
                self.message = "This message has been reported."
                self.likes = None
                self.dislikes = None
                self.creator = None
                self.report_flag = True
                return "Message reported successfully. Message has been taken down for review."
            else:
                self.report_count += 1
                return "Message reported successfully."
        else:
            return "You cannot report your own message."

    def delete(self, user):
        if user == self.creator or user.is_admin:
            self.message = "This message has been deleted."
            self.likes = None
            self.creator = None
        else:
            return "You cannot delete this message."

    def __str__(self):
        return f"{self.message} - {self.creator} ({self.likes} likes, {self.dislikes} dislikes)"
    
class announcement:
    def __init__(self, message, creator):
        self.message = message
        self.creator = creator
        self.priority = 1
        self.report_count = 0
        self.report_flag = False

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

    def delete(self, user):
        if user == self.creator or user.is_admin:
            self.message = "This announcement has been deleted."
            self.creator = None
        else:
            return "You cannot delete this announcement."

    def __str__(self):
        return f"{self.message} - {self.creator}"

class message_factory:
    @staticmethod
    def create_message(message_type, message, creator):
        if message_type == "standard":
            return standard_message(message, creator)
        elif message_type == "announcement":
            return announcement(message, creator)
        else:
            raise ValueError("Invalid message type")

