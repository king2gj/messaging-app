import os
import uuid

import mysql.connector
from mysql.connector import connect, Error
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

    def load_sql(self, path: str | Path) -> str:
        path = Path(path)
        return path.read_text(encoding="utf-8")

    def get_user_id_by_email(
            email: str,
            cursor) -> bytes:
        sql = load_sql("sql/users/get_id_by_email.sql")
        params = (email,)
        cursor.execute(sql, params)

        (user_id,) = cursor.fetchone()
        return user_id

# FOR INTERNAL USE ONLY. USE GROUP_ID IN PYTHON CODE
    def get_college_id_by_name(
            name: str,
            cursor) -> bytes:
        sql = load_sql("sql/colleges/get_id_by_name.sql")
        params = (name,)
        cursor.execute(sql, params)

        (college_id,) = cursor.fetchone()
        return college_id

    # FOR INTERNAL USE ONLY. USE GROUP_ID IN PYTHON CODE
    def get_course_id_by_course_code(
            course_code: str,
            cursor) -> bytes:
        sql = load_sql("sql/courses/get_id_by_course_code.sql")
        params = (course_code,)
        cursor.execute(sql, params)

        (course_id,) = cursor.fetchone()
        return course_id

    def add_new_user(
            user_id: bytes,
            username: str,
            email:str,
            bio: str,
            is_admin: bool,
            hashed_password: bytes,
            salt_code: str,
            cursor) -> None:
        if len(user_id) != 16:
            raise ValueError("ID must be 16 bytes")
        for x in {username, email}:
            if len(x) > 32:
                raise ValueError("Username and email cannot exceed 32 characters")
        if len(bio) > 160:
            raise ValueError("Bio cannot exceed 160 characters")
        if len(hashed_password) != 32:
            raise ValueError("Hashed password must be 32 bytes")
        if len(salt_code) > 32:
            raise ValueError("Salt code cannot exceed 32 characters")

        sql = load_sql("sql/users/create_new_user.sql")
        params = (user_id, username, email, bio, is_admin)
        cursor.execute(sql, params)

        sql = load_sql("sql/auth/create_new_auth.sql")
        params = (user_id, hashed_password, salt_code)
        cursor.execute(sql, params)

    def add_new_college(
            group_id: bytes,
            name: str,
            description: str,
            cursor) -> None:
        if len(group_id) != 16:
            raise ValueError("ID must be 16 bytes")
        if len(name) > 100:
            raise ValueError("College name cannot exceed 100 characters")
        if len(description) > 200:
            raise ValueError("Description cannot exceed 200 characters")

        college_id = uuid.uuid4().bytes

        sql = load_sql("sql/colleges/create_new_college.sql")
        params = (college_id, name, description)
        cursor.execute(sql, params)

        sql = load_sql("sql/message_groups/create_new_college_group.sql")
        params = (group_id, college_id)
        cursor.execute(sql, params)

    def add_new_course(
            group_id: bytes,
            course_code: str,
            name: str,
            description: str,
            offering_college_name: str,
            cursor) -> None:
        if len(group_id) != 16:
            raise ValueError("ID must be 16 bytes")
        if len(course_code) > 12:
            raise ValueError("Course code cannot exceed 12 characters")
        if len(name) > 100:
            raise ValueError("Course name cannot exceed 100 characters")
        if len(description) > 200:
            raise ValueError("Description cannot exceed 200 characters")

        course_id = uuid.uuid4().bytes
        college_id = get_college_id_by_name(offering_college_name, cursor)

        sql = load_sql("sql/courses/create_new_course.sql")
        params = (course_id, college_id, course_code, name, description)
        cursor.execute(sql, params)

        sql = load_sql("sql/message_groups/create_new_course_group.sql")
        params = (group_id, course_id)
        cursor.execute(sql, params)

        sql = load_sql("sql/colleges/increment_course_count.sql")
        params = (college_id,)
        cursor.execute(sql, params)

    def add_new_section(
            group_id: bytes,
            course_code: str,
            section_number: int,
            description: str,
            cursor) -> None:
        if len(group_id) != 16:
            raise ValueError("ID must be 16 bytes")
        if len(description) > 200:
            raise ValueError("Description cannot exceed 200 characters")

        section_id = uuid.uuid4().bytes
        course_id = get_course_id_by_course_code(course_code, cursor)

        sql = load_sql("sql/sections/create_new_section.sql")
        params = (section_id, course_id, section_number, description)
        cursor.execute(sql, params)

        sql = load_sql("sql/message_groups/create_new_section_group.sql")
        params = (group_id, section_id)
        cursor.execute(sql, params)

        sql = load_sql("sql/courses/increment_section_count.sql")
        params = (course_id,)
        cursor.execute(sql, params)

    def add_new_post(
            post_id: bytes,
            group_id: bytes,
            user_id: bytes,
            content: str,
            is_announcement: bool,
            cursor) -> None:
        for x in {post_id, group_id, user_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")
        if len(content) > 500:
            raise ValueError("Content cannot exceed 500 characters")

        sql = load_sql("sql/posts/create_new_post.sql")
        params = (post_id, group_id, user_id, content, is_announcement)
        cursor.execute(sql, params)

        sql = load_sql("sql/users/increment_post_count")
        params = (user_id,)
        cursor.execute(sql, params)

        sql = load_sql("sql/message_groups/increment_post_count")
        params = (group_id,)
        cursor.execute(sql, params)

    def add_new_comment(
            post_id: bytes,
            parent_post_id: bytes,
            group_id: bytes,
            user_id: bytes,
            content: bytes,
            cursor) -> None:
        for x in {post_id, parent_post_id, group_id, user_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")
        if len(content) > 500:
            raise ValueError("Content cannot exceed 500 characters")

        sql = load_sql("sql/posts/create_new_comment.sql")
        params = (post_id, parent_post_id, group_id, user_id, content)
        cursor.execute(sql, params)

        sql = load_sql("sql/posts/increment_comment_count.sql")
        params = (parent_post_id,)
        cursor.execute(sql, params)

    def add_new_report(
            report_id: bytes,
            reporter_id: bytes,
            post_id: bytes,
            report_content: str,
            cursor) -> None:
        for x in {report_id, reporter_id, post_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")
        if len(report_content) > 200:
            raise ValueError("Report content cannot exceed 200 characters")

        sql = load_sql("sql/reports/create_new_report.sql")
        params = (report_id, reporter_id, post_id, report_content)
        cursor.execute(sql, params)

        sql = load_sql("sql/posts/increment_report_count.sql")
        params = (post_id,)
        cursor.execute(sql, params)

    def add_user_to_group(
            user_id: bytes,
            group_id: bytes,
            role: str,
            cursor) -> None:
        for x in {user_id, group_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")
        if len(role) > 20:
            raise ValueError("Role cannot exceed 20 characters")

        sql = load_sql("sql/group_members/create_new_group_member.sql")
        params = (user_id, group_id, role)
        cursor.execute(sql, params)

        sql = load_sql("sql/message_groups/increment_member_count.sql")
        params = (group_id,)
        cursor.execute(sql, params)

    def add_like(
            user_id: bytes,
            post_id: bytes,
            cursor) -> None:
        for x in {user_id, post_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")

        sql = load_sql("sql/liked_posts/create_new_liked_post.sql")
        params = (user_id, post_id)
        cursor.execute(sql, params)

        sql = load_sql("sql/posts/increment_like_count.sql")
        params = (post_id,)
        cursor.execute(sql, params)

    def add_dislike(
            user_id: bytes,
            post_id: bytes,
            cursor) -> None:
        for x in {user_id, post_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")

        sql = load_sql("sql/disliked_posts/create_new_disliked_post.sql")
        params = (user_id, post_id)
        cursor.execute(sql, params)

        sql = load_sql("sql/posts/increment_dislike_count.sql")
        params = (post_id,)
        cursor.execute(sql, params)

    def add_file_to_post(
            media_id: bytes,
            post_id: bytes,
            file_path: str,
            cursor) -> None:
        for x in {media_id, post_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")
        if len(file_path) > 200:
            raise ValueError("File path cannot exceed 200 characters")

        sql = load_sql("sql/media/create_new_post_file.sql")
        params = (media_id, post_id, file_path)
        cursor.execute(sql, params)

    def add_profile_picture(
            media_id: bytes,
            user_id: bytes,
            file_path: str,
            cursor) -> None:
        for x in {media_id, user_id}:
            if len(x) != 16:
                raise ValueError("All IDs must be 16 bytes")
        if len(file_path) > 200:
            raise ValueError("File path cannot exceed 200 characters")

        sql = load_sql("sql/media/create_new_profile_picture.sql")
        params = (media_id, user_id, file_path)
        cursor.execute(sql, params)
        
    def user_login(email: str, password: str, cursor) -> bool:
        sql = load_sql("sql/authentication/user_login.sql")
        params = (email, password)
        cursor.execute(sql, params)
        result = cursor.fetchone()
        return result is not None

class access_database:
    def __init__(self, host=None, user=None, password=None, database=None, port=None):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.user = user or os.getenv("DB_USER", "python")
        self.password = password or os.getenv("DB_PASS", "python")
        self.database = database or os.getenv("DB_NAME", "auth")
        self.port = int(port or os.getenv("DB_PORT", 3306))

    def connect(self):
        try:
            conn = connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.database,
            )

            return conn
        except Error as e:
            print(e)
            return None
        
    def getuser(self, email: str, cursor):
        sql = load_sql("sql/authentication/get_user.sql")
        params = (email)
        cursor.execute(sql, params)
        result = cursor.fetchone()
        return result #this returned result should be the user object
    def newuser(self, email: str, password: str, username: str):
        try:
            conn = self.connect()
            if conn is None:
                print("Failed to connect to database.")
                return False
            with conn.cursor() as cur:
                sql = load_sql("sql/authentication/create_new_user.sql")
                params = (email, password)
                cur.execute(sql, params)
                conn.commit()
    
            return True
        except Error as e:
            print(e)
            return False
    def updateuser(self, email: str, password: str):
        try:
            conn = self.connect()
            if conn is None:
                print("Failed to connect to database.")
                return False
            with conn.cursor() as cur:
                sql = load_sql("sql/authentication/update_user.sql")
                params = (email, password, )
                cur.execute(sql, params)
                conn.commit()
    
            return True
        except Error as e:
            print(e)
            return False
if __name__ == "__main__":
    # quick runtime check when executing this file directly
    db = access_database()
    conn = db.connect()
    if conn:
        print("Connection established.")
        try:
            conn.close()
        except Exception:
            pass
    else:
        print("Failed to connect to database.")