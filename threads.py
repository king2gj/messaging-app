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

    def add_message(self, message):
        self.messages.append(message)
        self.message_count += 1
        self.last_message_date = datetime.datetime.now()
        self.last_message = message
