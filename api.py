from concurrent.futures import thread
import email
from unicodedata import name
from threads import thread
from flask import Flask, render_template, request, redirect, url_for, session
import database
import authenticator
board = Flask(__name__)



db = database.access_database()
conn = db.connect()

@board.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    return render_template(
        'home.html', 
        user_id=session['user_id']
    )

@board.route("/signup", methods=["GET", "POST"])
def signup():
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
    return render_template("signup.html")

@board.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        auth = authenticator.Authenticator()
        authed = auth.authenticate(email, password)
        if authed:
            user = db.get_user(email, conn.cursor())
            session["user_id"] = user.user_ID  
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials", 401
    return render_template("signin.html")
        

@board.route("/signout")
def signout():
    session.pop("user_id", None)
    return redirect(url_for("signin"))

@board.route("/account")
def account():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = db.get_user_by_id(session['user_id'], conn.cursor())
    return render_template("account.html", user=user)

@board.route("/update_account")
def update_account():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        authenticator.Authenticator.save_user_data(email, password)
        db.updateuser(email, password)
        return redirect(url_for("account"))
    return render_template("update_account.html")

@board.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        results = db.search_posts(query, conn.cursor())
        return render_template("search_results.html", results=results)
    return render_template("search.html")

@board.route("/view_post/<int:post_id>", methods=["GET"])
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
    
    

@board.route("/post") 
def post():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        newThread = thread(session['user_id'], title, content)
        db.create_post(session['user_id'], title, content, conn.cursor())
        return redirect(url_for("dashboard"))
    return render_template("create_post.html")


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