import datetime

class thread:
    def __init__(self, creator_ID, name, description, group_ID = None, course_code = None, section_ID = None, priority = 0):
        self.creator_ID = creator_ID
        self.name = name
        self.description = description
        self.course_code = course_code
        self.section_ID = section_ID
        self.group_ID = group_ID
        self.priority = priority
        self.members = [creator_ID]
        self.messages = []
        self.message_count = 0
        self.creation_date = datetime.datetime.now()
        self.last_message_date = None
        self.last_message = None
        self.is_active = True
        self.is_reported = False
        self.report_count = 0
        self.is_locked = False

    def add_message(self, message):
        if self.is_locked != True:
            if self.is_active == True:
                self.messages.append(message)
                self.message_count += 1
                self.last_message_date = datetime.datetime.now()
                self.last_message = message
            else:
                return "Thread is not active."
        else:
            return "Thread is locked."

    def add_member(self, member_ID):
        if self.is_locked != True:
            if self.is_active == True:
                self.members.append(member_ID)
            else:
                return "Thread is not active."
        else:
            return "Thread is locked."
        
    def remove_member(self, member_ID):
        if self.is_locked != True:
            if self.is_active == True:
                self.members.remove(member_ID)
            else:
                return "Thread is not active."
        else:
            return "Thread is locked."
        
    def remove_message(self, message_ID):
        if self.is_locked != True:
            if self.is_active == True:
                self.messages.remove(message_ID)
                self.message_count -= 1
            else:
                return "Thread is not active."
        else:
            return "Thread is locked."

    def report_thread(self):
        if self.report_count <= 3:
            self.is_reported = True
            self.report_count += 1
            return "Thread has been reported."
        else:
            self.is_active = False
            self.lock_thread()
            return "Thread has been deactivated due to too many reports."

    def activate_thread(self):
        self.is_active = True

    def deactivate_thread(self):
        self.is_active = False

    def lock_thread(self):
        self.is_active = False
        self.is_reported = True
        self.is_locked = True

    def display_thread(self):
        header =  f"Thread Name: {self.name}\nDescription: {self.description}\nCreation Date: {self.creation_date}\nMessage Count: {self.message_count}\nMembers: {self.members}\nIs Active: {self.is_active}\n"
        
        messages = "\n\n".join(message for message in self.messages)

        return f"{header}\n\n{messages}"



    
