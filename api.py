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
    return render_template(
        'home.html', 
        user_id=session['user_id']
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
        username = f"{first_name}{last_name}".lower() 
        password = request.form.get("password")
        auth = authenticator.Authenticator()
        result = auth.save_user_data(email, username, password)
        if result == "success":
            return redirect(url_for("signin"))
        elif result == "exists":
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
    user = database.get_user_object(session['user_id'], conn.cursor())
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

@board.route("/view_post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):  
    post = db.get_post(post_id, conn.cursor())
    if post:
        return render_template("view_post.html", post=post)
    else:
        return "Post not found", 404
    if request.method == "POST":
        content = request.form.get("content")
        db.add_reply(post_id, session['user_id'], content, conn.cursor())
        return redirect(url_for("view_post", post_id=post_id))


@board.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    if request.method == "POST":
        db.get_post(post_id, conn.cursor())
        if post.author_id != session['user_id']:
            return "Unauthorized", 403
        else:
            title = request.form.get("title")
            content = request.form.get("content")
            db.update_post(post_id, title, content, conn.cursor())
            return redirect(url_for("view_post", post_id=post_id))


if __name__ == '__main__':
    board.run(debug=True)