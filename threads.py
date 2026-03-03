import datetime
import uuid

class thread:
    def __init__(self, creator_ID, name, description, group_ID = None, course_code = None, section_ID = None, priority = 0):
        self.thread_ID = uuid.uuid4()
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
        self.is_deleted = False

    def add_message(self, message, user_ID):
        if user_ID in self.members:
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
        else:
            return "You are not a member of this thread."

    def add_member(self, member_ID, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == True:
                    self.members.append(member_ID)
                else:
                    return "Thread is not active."
            else:
                return "Thread is locked."
        else:
            return "You are not the creator of this thread."
        
    def make_creator(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == True:
                    if user_ID in self.members:
                        self.creator_ID = user_ID
                else:
                    return "Thread is not active."
            else:
                return "Thread is locked."
        else:
            return "You are not the creator of this thread."
        
    def remove_member(self, member_ID, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == True:
                    if member_ID in self.members:
                        if member_ID == self.creator_ID:
                            return "You cannot remove yourself as the creator of this thread."
                        else:
                            self.members.remove(member_ID)
                    else:
                        return "Member is not in the thread."
                else:
                    return "Thread is not active."
            else:
                return "Thread is locked."
        else:
            return "You are not the creator of this thread."
        
    def remove_message(self, message):
        if self.is_locked != True:
            if self.is_active == True:
                self.messages.remove(message)
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

    def activate_thread(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == False:
                    self.is_active = True
                else:
                    return "Thread is already active."
            else:
                return "Thread is locked."
        else:
            return "You are not the creator of this thread."

    def deactivate_thread(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == True:
                    self.is_active = False
                else:
                    return "Thread is already deactivated."
            else:
                return "Thread is locked."
        else:
            return "You are not the creator of this thread."

    def lock_thread(self):
        self.is_active = False
        self.is_reported = True
        self.is_locked = True

    def display_thread(self):
        header =  f"Thread Name: {self.name}\nDescription: {self.description}\nCreation Date: {self.creation_date}\nMessage Count: {self.message_count}\nMembers: {self.members}\nIs Active: {self.is_active}\n"
        
        messages = "\n\n".join(str(message) for message in self.messages)

        if self.is_deleted:
            return "Thread has been deleted."
        else:
            if self.is_locked == True:
                return f"{header}\n\nThread is locked."
            else:
                return f"{header}\n\n{messages}"
    
    def edit_thread(self, user_ID, name, description, group_ID = None, course_code = None, section_ID = None, priority = 0):
        if user_ID == self.creator_ID:    
            if self.is_locked != True:
                if self.is_active == True:
                    self.name = name
                    self.description = description
                    self.group_ID = group_ID
                    self.course_code = course_code
                    self.section_ID = section_ID
                    self.priority = priority
                else:
                    return "Thread is not active."
            else:
                return "Thread is locked."
        else:
            return "You are not the creator of this thread."
    
    def __str__(self):
        return self.display_thread()
    
    def delete_thread(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == True:
                    # wipe all self attributes to none
                    self.creator_ID = None
                    self.name = None
                    self.description = None
                    self.course_code = None
                    self.section_ID = None
                    self.group_ID = None
                    self.priority = None
                    self.members = None
                    self.messages = None
                    self.message_count = None
                    self.creation_date = None
                    self.last_message_date = None
                    self.last_message = None
                    self.is_active = None
                    self.is_reported = None
                    self.report_count = None
                    self.is_locked = None
                    self.is_deleted = True
                    return "Thread has been deleted."
                else:
                    return "Thread is not active."
            else:
                return "Thread is locked."
        else:
            return "You are not the creator of this thread."



    
