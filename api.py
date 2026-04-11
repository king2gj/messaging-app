from concurrent.futures import thread
import email
from unicodedata import name
from threads import thread
from flask import Flask, render_template, request, redirect, url_for, session
import database
import authenticator
board = Flask(__name__)
board.secret_key = "donthackus"


db = database.access_database()
conn = db.connect()

@board.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('signin', error="User not logged in, Please sign in to access the dashboard."))
    error = request.args.get("error")
    return render_template(
        'home.html', 
        posts=database.get_all_posts(session['user_id']),
        courses=database.get_course_by_user(session['user_id']),
        user_id=session['user_id'],
        error=error
    )

@board.route("/signup", methods=["GET", "POST"])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = request.args.get("error")
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        username = request.form.get("username")
        password = request.form.get("password")
        auth = authenticator.Authenticator()
        result = auth.save_user_data(email, first_name, last_name, username, password)
        if result == "success":
            return redirect(url_for("signin"))
        elif result == "emailexists":
            return render_template("signup.html", error="An account with that email already exists.")
        else:
            return render_template("signup.html", error="An error occurred. Please try again.")
    return render_template("signup.html", error=error)

@board.route("/signin", methods=["GET", "POST"])
def signin():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = request.args.get("error") 
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        auth = authenticator.Authenticator()
        authed = auth.authenticate(email, password)
        if authed:
            user_id = database.get_user_id_by_email(email)
            session["user_id"] = user_id
            return redirect(url_for("dashboard"))
        else:
            return render_template("signin.html", error="Invalid credentials.")
    return render_template("signin.html", error=error)
        

@board.route("/signout")
def signout():
    session.pop("user_id", None)
    return redirect(url_for("signin"))

@board.route("/account")
def account():
    if 'user_id' not in session:
        return redirect(url_for('signin', error="User not logged in, Please sign in to access your account."))
    print(f"session user_id: {session['user_id']}, type: {type(session['user_id'])}")
    user = database.get_user_object(session['user_id'])
    return render_template("account.html", user=user)

@board.route("/account_edit", methods=["GET", "POST"])
def update_account():
    if 'user_id' not in session:
        return redirect(url_for('signin', error="User not logged in, Please sign in to access your account."))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        authenticator.Authenticator.save_user_data(email, password)
        db.updateuser(email, password)
        return redirect(url_for("account"))
    return render_template("account_edit.html")
@board.route("/posts")
def posts_page():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    course_id = request.args.get("course_id")
    posts = database.get_posts_by_course(bytes.fromhex(course_id)) if course_id else database.get_all_posts(session['user_id'])
    courses = database.get_course_by_user(session['user_id'])
    return render_template('posts.html', posts=posts, courses=courses, active_course=course_id)
@board.route("/create_post", methods=["GET", "POST"]) 
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        tags = request.form.get("tags")
        new_thread = thread(
            title=title,
            creator_ID=session['user_id'],
            creator_name=database.get_user_object(session['user_id']).username,
            content=content
        )
        try:
            database.add_new_post(new_thread)
            return redirect(url_for("dashboard"))
        except Exception as e:
            print(f"Error creating post: {e}")
            return render_template("create_post.html", error="An error occurred while creating the post. Please try again.")
    return render_template("create_post.html")
@board.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        results = db.search_posts(query, conn.cursor())
        return render_template("search_results.html", results=results)
    return render_template("search.html")

@board.route("/view_post/<post_id>", methods=["GET", "POST"])
def view_post(post_id):  
    print(f"Viewing post with ID: {post_id}, type: {type(post_id)}")
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    post = database.get_post_by_id(bytes.fromhex(post_id))
    if not post:
        return "Post not found", 404
    return render_template("view_post.html", post=post)

@board.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    if request.method == "POST":
        db.get_post(post_id, conn.cursor())
        if post.author_id != session['user_id']:
            return render_template("home.html", error="You do not have permission to access this page.")
        else:
            title = request.form.get("title")
            content = request.form.get("content")
            db.update_post(post_id, title, content, conn.cursor())
            return redirect(url_for("view_post", post_id=post_id))


@board.route("/admin/enroll", methods=["GET", "POST"])
def admin_enroll():
    if 'user_id' not in session:
        return redirect(url_for('signin',))
    # check if user is admin
    user = database.get_user_object(session['user_id'])
    if not bool(user.is_admin):
        return redirect(url_for('dashboard', error="You do not have permission to access this page."))
    selected_user_id = request.args.get("selected_user")
    courses = database.get_all_courses(bytes.fromhex(selected_user_id)) if selected_user_id else []

    if request.method == "POST":
        target_user_id = bytes.fromhex(request.form.get("user_id"))
        group_id = bytes.fromhex(request.form.get("group_id"))
        role = request.form.get("is_faculty") or "student"  # "faculty" if checked, "student" if not
        result = database.add_user_to_course(target_user_id, group_id, role)
        remaining_courses = database.get_all_courses(target_user_id)
        target_user_hex = request.form.get("user_id")
        if result:
            return render_template("admin_enroll.html",
                success="User enrolled successfully.",
                users=database.get_all_users(),
                courses=remaining_courses,
                selected_user=target_user_hex)
        else:
            return render_template("admin_enroll.html",
                error="Failed to enroll user.",
                users=database.get_all_users(),
                courses=remaining_courses,
                selected_user=target_user_hex)
    
    return render_template("admin_enroll.html",
        users=database.get_all_users(),
        courses=courses,
        selected_user=selected_user_id)


if __name__ == '__main__':
    board.run(debug=True)