import datetime
import uuid

class Course:
    def __init__(self, name, creator_ID, priority = 0, description = None, college_ID = None, course_code = None):
        self.course_id = uuid.uuid4()
        self.creator_ID = creator_ID
        self.college_ID = college_ID
        self.course_code = course_code
        self.members = [creator_ID]
        self.name = name
        self.description = description
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None
        self.is_deleted = False
        self.thread_count = 0
        self.section_count = 0
        self.group_count = 0
        self.message_count = 0
        self.member_count = 1
        self.priority = priority
        self.threads = []
        self.sections = []
        self.groups = []
        self.messages = []
        self.is_active = True
        self.is_reported = False
        self.report_count = 0
        self.is_locked = False
        self.is_deleted = False

    def add_thread(self, thread: Thread):
        if not isinstance(thread, Thread):
            raise ValueError(f"Expected Thread, got {type(thread).__name__}")
        elif thread.thread_ID in self.threads:
            raise ValueError(f"Thread {thread.thread_ID} already exists in this course.")
        else:
            self.threads.append(thread.thread_ID)
            self.thread_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_thread(self, thread_ID):
        if thread_ID not in self.threads:
            raise ValueError(f"Thread {thread_ID} does not exist in this course.")
        else:
            self.threads.remove(thread_ID)
            self.thread_count -= 1
            self.updated_at = datetime.datetime.now()

    def add_section(self, section: Section):
        if not isinstance(section, Section):
            raise ValueError(f"Expected Section, got {type(section).__name__}")
        elif section.section_ID in self.threads:
            raise ValueError(f"Section {section.section_ID} already exists in this course.")
        else:
            self.sections.append(section.section_ID)
            self.section_count_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_section(self, section_ID):
        if section_ID not in self.threads:
            raise ValueError(f"Section {section_ID} does not exist in this course.")
        else:
            self.sections.remove(section_ID)
            self.section_count_count -= 1
            self.updated_at = datetime.datetime.now()

    def add_group(self, group: Group):
        if not isinstance(group, Group):
            raise ValueError(f"Expected Group, got {type(group).__name__}")
        elif group.group_ID in self.groups:
            raise ValueError(f"Group {group.group_ID} already exists in this course.")
        else:
            self.groups.append(group.group_ID)
            self.group_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_group(self, group_ID):
        if group_ID not in self.groups:
            raise ValueError(f"Group {group_ID} does not exist in this course.")
        else:
            self.groups.remove(group_ID)
            self.group_count -= 1
            self.updated_at = datetime.datetime.now()
    
    def add_message(self, message):
        if not isinstance(message, Message):
            raise ValueError(f"Expected Message, got {type(message).__name__}")
        elif message in self.messages:
            raise ValueError(f"Message {message.message_ID} already exists in this course.")
        else:
            self.messages.append(message)
            self.message_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_message(self, message):
        if message not in self.messages:
            raise ValueError(f"Message {message.message_ID} does not exist in this course.")
        else:
            self.messages.remove(message)
            self.message_count -= 1
            self.updated_at = datetime.datetime.now()

    def add_member(self, user):
        if not isinstance(user, standard_user):
            raise ValueError(f"Expected standard_user, got {type(user).__name__}")
        elif user.user_ID in self.members:
            raise ValueError(f"User {user.user_ID} already exists in this course.")
        else:
            self.members.append(user.user_ID)
            self.member_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_member(self, user_ID):
        if user_ID not in self.members:
            raise ValueError(f"User {user_ID} does not exist in this course.")
        else:
            self.members.remove(user_ID)
            self.member_count -= 1
            self.updated_at = datetime.datetime.now()

    def report(self):
        if self.report_count <= 3:
            self.is_reported = True
            self.report_count += 1
            return "Course has been reported."
        else:
            self.is_active = False
            self.lock_thread()
            return "Course has been deactivated due to too many reports."

    def activate(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == False:
                    self.is_active = True
                else:
                    return "Course is already active."
            else:
                return "Course is locked."
        else:
            return "You are not the creator of this course."

    def deactivate(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == True:
                    self.is_active = False
                else:
                    return "Course is already deactivated."
            else:
                return "Course is locked."
        else:
            return "You are not the creator of this Course."

    def lock(self):
        self.is_active = False
        self.is_reported = True
        self.is_locked = True

    def display(self):
        header =  f"Course Name: {self.name}\nDescription: {self.description}\nCourse Code: {self.course_code}\n Offering College: {self.college_ID}\nCreation Date: {self.created_at}\nLast Updated: {self.updated_at}\nSection Count: {self.section_count}\nGroup Count: {self.group_count}\nMessage Count: {self.message_count}\nMember Count: {self.member_count}\nIs Active: {self.is_active}\n"
        
        sections = "\n\n".join(str(section) for section in self.sections)

        groups = "\n\n".join(str(group) for group in self.groups)

        threads = "\n\n".join(str(thread) for thread in self.threads)
        
        messages = "\n\n".join(str(message) for message in self.messages)

        if self.is_deleted:
            return "Thread has been deleted."
        else:
            if self.is_locked == True:
                return f"{header}\n\nThread is locked."
            else:
                return f"{header}\n\n{sections}\n\n{groups}\n\n{threads}\n\n{messages}"
            
    def __str__(self):
        self.display_course()
    

class Section:
    def __init__(self, name, creator_ID, priority = 0, description = None, course_code = None):
        self.section_id = uuid.uuid4()
        self.creator_ID = creator_ID
        self.course_code = course_code
        self.members = [creator_ID]
        self.name = name
        self.description = description
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None
        self.is_deleted = False
        self.thread_count = 0
        self.group_count = 0
        self.message_count = 0
        self.member_count = 1
        self.priority = priority
        self.threads = []
        self.groups = []
        self.messages = []
        self.is_active = True
        self.is_reported = False
        self.report_count = 0
        self.is_locked = False
        self.is_deleted = False

    def add_thread(self, thread: Thread):
        if not isinstance(thread, Thread):
            raise ValueError(f"Expected Thread, got {type(thread).__name__}")
        elif thread.thread_ID in self.threads:
            raise ValueError(f"Thread {thread.thread_ID} already exists in this section.")
        else:
            self.threads.append(thread.thread_ID)
            self.thread_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_thread(self, thread_ID):
        if thread_ID not in self.threads:
            raise ValueError(f"Thread {thread_ID} does not exist in this section.")
        else:
            self.threads.remove(thread_ID)
            self.thread_count -= 1
            self.updated_at = datetime.datetime.now()

    def add_group(self, group: Group):
        if not isinstance(group, Group):
            raise ValueError(f"Expected Group, got {type(group).__name__}")
        elif group.group_ID in self.groups:
            raise ValueError(f"Group {group.group_ID} already exists in this section.")
        else:
            self.groups.append(group.group_ID)
            self.group_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_group(self, group_ID):
        if group_ID not in self.groups:
            raise ValueError(f"Group {group_ID} does not exist in this section.")
        else:
            self.groups.remove(group_ID)
            self.group_count -= 1
            self.updated_at = datetime.datetime.now()
    
    def add_message(self, message):
        if not isinstance(message, Message):
            raise ValueError(f"Expected Message, got {type(message).__name__}")
        elif message in self.messages:
            raise ValueError(f"Message {message.message_ID} already exists in this section.")
        else:
            self.messages.append(message)
            self.message_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_message(self, message):
        if message not in self.messages:
            raise ValueError(f"Message {message.message_ID} does not exist in this section.")
        else:
            self.messages.remove(message)
            self.message_count -= 1
            self.updated_at = datetime.datetime.now()

    def add_member(self, user):
        if not isinstance(user, standard_user):
            raise ValueError(f"Expected standard_user, got {type(user).__name__}")
        elif user.user_ID in self.members:
            raise ValueError(f"User {user.user_ID} already exists in this section.")
        else:
            self.members.append(user.user_ID)
            self.member_count += 1
            self.updated_at = datetime.datetime.now()

    def remove_member(self, user_ID):
        if user_ID not in self.members:
            raise ValueError(f"User {user_ID} does not exist in this section.")
        else:
            self.members.remove(user_ID)
            self.member_count -= 1
            self.updated_at = datetime.datetime.now()

    def report(self):
        if self.report_count <= 3:
            self.is_reported = True
            self.report_count += 1
            return "Section has been reported."
        else:
            self.is_active = False
            self.lock_thread()
            return "Section has been deactivated due to too many reports."

    def activate(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == False:
                    self.is_active = True
                else:
                    return "Section is already active."
            else:
                return "Section is locked."
        else:
            return "You are not the creator of this Section."

    def deactivate(self, user_ID):
        if user_ID == self.creator_ID:
            if self.is_locked != True:
                if self.is_active == True:
                    self.is_active = False
                else:
                    return "Section is already deactivated."
            else:
                return "Section is locked."
        else:
            return "You are not the creator of this section."

    def lock(self):
        self.is_active = False
        self.is_reported = True
        self.is_locked = True

    def display(self):
        header =  f"Section Name: {self.name}\nDescription: {self.description}\nCourse Code: {self.course_code}\nCreation Date: {self.created_at}\nLast Updated: {self.updated_at}\nGroup Count: {self.group_count}\nMessage Count: {self.message_count}\nMember Count: {self.member_count}\nIs Active: {self.is_active}\n"

        groups = "\n\n".join(str(group) for group in self.groups)

        threads = "\n\n".join(str(thread) for thread in self.threads)
        
        messages = "\n\n".join(str(message) for message in self.messages)

        if self.is_deleted:
            return "Thread has been deleted."
        else:
            if self.is_locked == True:
                return f"{header}\n\nThread is locked."
            else:
                return f"{header}\n\n{groups}\n\n{threads}\n\n{messages}"
            
    def __str__(self):
        self.display()