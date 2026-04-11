import os
from unittest import result
import uuid
import users
import threads
import datetime
import mysql.connector
from mysql.connector import connect, Error
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

class access_database:
    def __init__(self, host=None, user=None, password=None, database=None, port=None):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.user = user or os.getenv("DB_USER", "root")
        self.password = password or os.getenv("DB_PASS", "root")
        self.database = database or os.getenv("DB_NAME", "message_board")
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
db = access_database()
conn = db.connect()

BASE_DIR = Path(__file__).parent

def load_sql(path: str | Path) -> str:
    full_path = BASE_DIR / path
    return full_path.read_text(encoding="utf-8")

def get_user_id_by_email(email: str,) -> bytes:
        sql = load_sql("sql/users/get_id_by_email.sql")
        params = (email,)
        cursor = conn.cursor(buffered=True) 
        cursor.execute(sql, params)
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]
def get_user_auth_info_by_id(user_id: bytes) -> tuple[bytes, str]:
    sql = load_sql("sql/auth/get_auth_info.sql")
    params = (user_id,)
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, params)

    result = cursor.fetchone()
    print(f"Auth info for user ID {user_id}: {result}")
    if result is None:
        raise ValueError("No auth info found for given user ID")

    hashed_password, salt_code = result
    return hashed_password, salt_code
def add_new_user(
            username: str,
            first_name: str,
            last_name: str,
            email:str,
            bio: str,
            is_admin: bool,
            hashed_password: bytes,
            salt_code: str,) -> None:
        

        newUser = users.StandardUser()
        newUser.user_ID = uuid.uuid4().bytes
        newUser.username = username
        newUser.first_name = first_name
        newUser.last_name = last_name
        newUser.email = email
        newUser.bio = bio
        newUser.is_admin = is_admin
        newUser.password = hashed_password
        newUser.salt_code = salt_code

        if len(newUser.user_ID) != 16:
            raise ValueError("ID must be 16 bytes")
        for x in {newUser.username, newUser.email}:
            if len(x) > 32:
                raise ValueError("Username and email cannot exceed 32 characters")
        if len(newUser.bio) > 160:
            raise ValueError("Bio cannot exceed 160 characters")
        if len(newUser.password) != 32:
            raise ValueError("Hashed password must be 32 bytes")
        if len(newUser.salt_code) > 32:
            raise ValueError("Salt code cannot exceed 32 characters")

        sql = load_sql("sql/users/create_new_user.sql")
        params = (newUser.user_ID, newUser.username, newUser.email, newUser.bio, newUser.is_admin, newUser.first_name, newUser.last_name)
        conn.cursor().execute(sql, params)
        conn.commit()

        sql = load_sql("sql/auth/create_new_auth.sql")
        params = (newUser.user_ID, newUser.password, newUser.salt_code)
        conn.cursor().execute(sql, params)
        conn.commit()
def get_all_users():
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT user_id, username, email FROM users ORDER BY username ASC")
    return cursor.fetchall()    

def add_new_post(post) -> None:
    for x in {post.post_id.bytes, post.creator_ID}:
        if len(x) != 16:
            raise ValueError("All IDs must be 16 bytes")
    if len(post.content) > 500:
        raise ValueError("Content cannot exceed 500 characters")

    sql = load_sql("sql/posts/create_new_post.sql")
    params = (post.title, post.post_id.bytes, post.creator_ID, post.creator_name, post.content, post.announcement, post.group_ID)
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, params)
    conn.commit()
    sql = load_sql("sql/users/increment_post_count.sql")
    params = (post.creator_ID,)
    cursor.execute(sql, params)
    conn.commit()
    # sql = load_sql("sql/message_groups/increment_post_count")
    # params = (post.group_ID,)
    # cursor.execute(sql, params)
    # conn.commit()
def get_all_posts(user_id: bytes):
    sql = load_sql("sql/posts/get_all_posts.sql")
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql)
    rows = cursor.fetchall()

    posts = []
    for row in rows:
        post = threads.thread(
            title=row[1],
            creator_ID=row[6],
            creator_name=row[6],
            content=row[2],
        )
        post.post_id = row[0].hex()
        post.creation_date = row[3]
        post.like_count = row[4]
        post.comment_count = row[5]
        post.creator_name = row[6]
        posts.append(post)
    return posts


def get_post_by_id(post_id: bytes):
    sql = load_sql("sql/posts/get_post_by_id.sql")
    params = (post_id,)
    cursor = conn.cursor(buffered=True)
    row = cursor.execute(sql, params)
    row = cursor.fetchone()
    if row is None:
        return None
    class viewPost:
        pass
    post = viewPost()
    post.post_id = row[0].hex()
    post.title = row[1]
    post.content = row[2]
    post.created_at = row[3]
    post.like_count = row[4]
    post.comment_count = row[5]
    post.username = row[6]
    post.dislike_count = 0
    post.comments = []
    post.creator_id = None

    return post
def get_posts_by_course(course_id: bytes):
    sql = load_sql("sql/posts/get_posts_by_course.sql")
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, (course_id,))
    rows = cursor.fetchall()
    posts = []
    for row in rows:
        post = threads.thread(
            title=row[1],
            creator_ID=row[6],
            creator_name=row[6],
            content=row[2],
        )
        post.post_id = row[0].hex()
        post.creation_date = row[3]
        post.like_count = row[4]
        post.comment_count = row[5]
        post.creator_name = row[6]
        posts.append(post)
    return posts
# FOR INTERNAL USE ONLY. USE GROUP_ID IN PYTHON CODE
def get_course_by_user(user_id: bytes):
    sql = load_sql("sql/courses/get_courses_by_user.sql")
    params = (user_id,)
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, params)
    return cursor.fetchall()
def get_all_courses(user_id: bytes):
    sql = load_sql("sql/courses/get_all_courses.sql")
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, (user_id,))
    return cursor.fetchall()
def add_user_to_course(user_id: bytes, course_code: str, role: str):
    try:
        sql = load_sql("sql/courses/add_user_to_course.sql")
        if role not in {"student", "faculty"}:
            raise ValueError("Role must be 'student' or 'faculty'")
        if role == "faculty":
            role = "Faculty"
        elif role == "student":
            role = "Student"
        params = (user_id, course_code, role)
        cursor = conn.cursor(buffered=True)
        cursor.execute(sql, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user to course: {e}")
        return False
def get_college_id_by_name(
            name: str,
            cursor) -> bytes:
        sql = load_sql("sql/colleges/get_id_by_name.sql")
        params = (name,)
        conn.cursor().execute(sql, params)

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
    conn.cursor.execute(sql, params)
    conn.commit()
    sql = load_sql("sql/message_groups/create_new_section_group.sql")
    params = (group_id, section_id)
    conn.cursor.execute(sql, params)
    conn.commit()
    sql = load_sql("sql/courses/increment_section_count.sql")
    params = (course_id,)
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

def get_user_object(
        user_id: bytes ) -> users.StandardUser | None:
    sql = load_sql("sql/users/get_user_info.sql")
    params = (user_id,)
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, params)

    raw_data = cursor.fetchone()
    print(f"get_user_object raw_data: {raw_data}")
    if raw_data is None:
        return None

    columns = [col[0] for col in cursor.description]
    dict_data = dict(zip(columns, raw_data))
    print(f"raw is_admin from db: {dict_data['is_admin']}, type: {type(dict_data['is_admin'])}")

    user_kwargs = {
        "user_ID": uuid.UUID(bytes=dict_data["user_id"]),
        "username": dict_data["username"],
        "first_name": dict_data["first_name"],
        "last_name": dict_data["last_name"],
        "email": dict_data["email"],
        "bio": dict_data["bio"],
        "post_count": dict_data["post_count"],
        "is_admin": dict_data["is_admin"],
        "date_joined": dict_data["created_at"],
        "auth_success": True
    }

    return users.StandardUser(**user_kwargs)

def edit_post(
        post_id: bytes,
        content: str) -> None:
    sql = load_sql("sql/posts/update_post.sql")
    params = (content, post_id)

    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, params)
    conn.commit()

def edit_profile(
        user_id: bytes,
        username: str,
        email: str,
        bio: str) -> None:
    sql = load_sql("sql/users/edit_user.sql")
    params = (username, email, bio, user_id)

    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, params)
    conn.commit()

def edit_pfp(
        user_id: bytes,
        file_path: str) -> None:
    sql = load_sql("sql/media/edit_pfp.sql")
    params = (file_path, user_id)

    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, params)
    conn.commit()

def get_all_posts_by_user(user_id: bytes):
    sql = load_sql("sql/posts/get_all_posts_made_by_user.sql")
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql, (user_id,))
    return cursor.fetchall()