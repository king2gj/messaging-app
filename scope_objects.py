import datetime
import uuid

'''
1. All IDs are object_ID (college, course, section).
2. Scopes are college, course, section, message(sub-class comment).
3. Member list stores tuples of (user_ID, role).
'''

class College:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not hasattr(self, "object_ID"):
            self.object_ID = uuid.uuid4()

        if not hasattr(self, "creator_ID"):
            self.creator_ID = None

        if not hasattr(self, "name"):
            self.name = None

        if not hasattr(self, "description"):
            self.description = None

        if not hasattr(self, "member_list"):
            self.member_list = [(self.creator_ID, "creator")]

        if not hasattr(self, "course_list"):
            self.course_list = []

        if not hasattr(self, "message_list"):
            self.message_list = []

        if not hasattr(self, "post_count"):
            self.post_count = len(self.message_list)

        if not hasattr(self, "member_count "):
            self.member_count = len(self.member_list)

        if not hasattr(self, "course_count"):
            self.course_count = len(self.section_list)

        if not hasattr(self, "created_at"):
            self.created_at = datetime.datetime.now()

        if not hasattr(self, "is_active"):
            self.is_active = True

        if not hasattr(self, "report_count"):
            self.report_count = 0

        self.is_reported = True if self.report_count > 0 else False

        self.is_locked = True if self.report_count >= 3 else False
              

    def add_member(self, user, role = "member"):
        if (user.user_ID, role) not in self.member_list:
            self.member_list.append((user.user_ID, role))
            return True
        else:
            return False

    def remove_member(self, user_ID):
        for member in self.member_list:
            if member[0] == user_ID:
                self.member_list.remove(member)
                return True
        return False

    def add_course(self, course_ID):
        if course_ID not in self.course_list:
            self.course_list.append(course_ID)
            return True
        else:
            return False

    def remove_course(self, course_ID):
        if course_ID in self.course_list:
            self.course_list.remove(course_ID)
            return True
        else:
            return False

    def add_message(self, message_ID):
        if message_ID not in self.message_list:
            self.message_list.append(message_ID)
            return True
        else:
            return False

    def remove_message(self, message_ID):
        if message_ID in self.message_list:
            self.message_list.remove(message_ID)
            return True
        else:
            return False

    def report(self):
        self.report_count += 1
        self.is_reported = True
        if self.report_count >= 3:
            self.is_locked = True

    def unlock(self):
        self.report_count = 0
        self.is_reported = False
        self.is_locked = False

    def __str__(self):
        header = f"College Name: {self.name}\nDescription: {self.description}\nCreated At: {self.created_at.strftime('%b-%d-%Y')}\nIs Active: {self.is_active}"

        if self.is_locked:
            return header + "\nThis college has been locked due to multiple reports."

        member_list = "\n".join([f"{member[0]} - {member[1]}" for member in self.member_list])
        course_list = "\n".join(self.course_list)
        message_list = "\n".join(self.message_list)

        return f"{header}\n\nMembers:\n{member_list}\n\nCourses:\n{course_list}\n\nMessages:\n{message_list}"
    

class Course:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not hasattr(self, "object_ID"):
            self.object_ID = uuid.uuid4()

        if not hasattr(self, "parent_ID"):
            self.offering_college = None

        if not hasattr(self, "course_code"):
            self.creator_ID = None

        if not hasattr(self, "creator_ID"):
            self.creator_ID = None

        if not hasattr(self, "name"):
            self.name = None

        if not hasattr(self, "description"):
            self.description = None

        if not hasattr(self, "member_list"):
            self.member_list = [self.creator_ID]

        if not hasattr(self, "section_list"):
            self.section_list = []

        if not hasattr(self, "message_list"):
            self.message_list = []

        if not hasattr(self, "post_count"):
            self.post_count = len(self.message_list)

        if not hasattr(self, "member_count "):
            self.member_count = len(self.member_list)

        if not hasattr(self, "section_count"):
            self.section_count = len(self.section_list)

        if not hasattr(self, "created_at"):
            self.created_at = datetime.datetime.now()

        if not hasattr(self, "is_active"):
            self.is_active = True

        if not hasattr(self, "report_count"):
            self.report_count = 0

        self.is_reported = True if self.report_count > 0 else False

        self.is_locked = True if self.report_count >= 3 else False
              

    def add_member(self, user, role = "member"):
        if (user.user_ID, role) not in self.member_list:
            self.member_list.append((user.user_ID, role))
            return True
        else:
            return False

    def remove_member(self, user_ID):
        for member in self.member_list:
            if member[0] == user_ID:
                self.member_list.remove(member)
                return True
        return False

    def add_section(self, section_ID):
        if section_ID not in self.section_list:
            self.section_list.append(section_ID)
            return True
        else:
            return False

    def remove_section(self, section_ID):
        if section_ID in self.section_list:
            self.section_list.remove(section_ID)
            return True
        else:
            return False

    def add_message(self, message_ID):
        if message_ID not in self.message_list:
            self.message_list.append(message_ID)
            return True
        else:
            return False

    def remove_message(self, message_ID):
        if message_ID in self.message_list:
            self.message_list.remove(message_ID)
            return True
        else:
            return False

    def report(self):
        self.report_count += 1
        self.is_reported = True
        if self.report_count >= 3:
            self.is_locked = True

    def unlock(self):
        self.report_count = 0
        self.is_reported = False
        self.is_locked = False

    def __str__(self):
        header = f"Course Name: {self.name}\nCourse Code: {self.course_code}\nOffering College: {self.offering_college}\nDescription: {self.description}\nCreated At: {self.created_at.strftime('%b-%d-%Y')}\nIs Active: {self.is_active}"

        if self.is_locked:
            return header + "\nThis college has been locked due to multiple reports."

        member_list = "\n".join([f"{member[0]} - {member[1]}" for member in self.member_list])
        section_list = "\n".join(self.section_list)
        message_list = "\n".join(self.message_list)

        return f"{header}\n\nMembers:\n{member_list}\n\nCourses:\n{section_list}\n\nMessages:\n{message_list}"


class Section:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not hasattr(self, "object_ID"):
            self.object_ID = uuid.uuid4()

        if not hasattr(self, "offering_college"):
            self.offering_college = None

        if not hasattr(self, "parent_ID"):
            self.parent_ID  = None

        if not hasattr(self, "creator_ID"):
            self.creator_ID = None

        if not hasattr(self, "name"):
            self.name = None

        if not hasattr(self, "description"):
            self.description = None

        if not hasattr(self, "member_list"):
            self.member_list = [self.creator_ID]

        if not hasattr(self, "message_list"):
            self.message_list = []

        if not hasattr(self, "created_at"):
            self.created_at = datetime.datetime.now()

        if not hasattr(self, "is_active"):
            self.is_active = True

        if not hasattr(self, "report_count"):
            self.report_count = 0

        if not hasattr(self, "post_count"):
            self.post_count = len(self.message_list)

        if not hasattr(self, "member_count "):
            self.member_count = len(self.member_list)

        self.is_reported = True if self.report_count > 0 else False

        self.is_locked = True if self.report_count >= 3 else False
              

    def add_member(self, user, role = "member"):
        if (user.user_ID, role) not in self.member_list:
            self.member_list.append((user.user_ID, role))
            return True
        else:
            return False

    def remove_member(self, user_ID):
        for member in self.member_list:
            if member[0] == user_ID:
                self.member_list.remove(member)
                return True
        return False

    def add_message(self, message_ID):
        if message_ID not in self.message_list:
            self.message_list.append(message_ID)
            return True
        else:
            return False

    def remove_message(self, message_ID):
        if message_ID in self.message_list:
            self.message_list.remove(message_ID)
            return True
        else:
            return False

    def report(self):
        self.report_count += 1
        self.is_reported = True
        if self.report_count >= 3:
            self.is_locked = True

    def unlock(self):
        self.report_count = 0
        self.is_reported = False
        self.is_locked = False

    def __str__(self):
        header = f"Section Name: {self.name}\nCourse: {self.parent_ID}\nOffering College: {self.offering_college}\nDescription: {self.description}\nCreated At: {self.created_at.strftime('%b-%d-%Y')}\nIs Active: {self.is_active}"

        if self.is_locked:
            return header + "\nThis section has been locked due to multiple reports."

        member_list = "\n".join([f"{member[0]} - {member[1]}" for member in self.member_list])
        message_list = "\n".join(self.message_list)

        return f"{header}\n\nMembers:\n{member_list}\n\nMessages:\n{message_list}"


