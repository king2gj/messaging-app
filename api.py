from concurrent.futures import thread
from unicodedata import name
from threads import Thread
from flask import Flask, render_template, request, redirect, url_for, session
import database, authenticator
app = Flask(__name__)
app.run
db = database.access_database()
conn = db.connect()

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    return render_template(
        'dashboard.html', 
        user_id=session['user_id']
    )


@app.route("/")
def index(name=None):
    return render_template('base_post.html', person=name)


@app.route("/signup")
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        saved = authenticator.save_user_data(email, username, password)
        if saved:
            return redirect(url_for("signin"))
        else:
            return "Error saving user data", 500
    return render_template("signup.html")

@app.route("/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        authenticator = authenticator.authenticate(email, password)
        if authenticator:
            user = db.get_user(email, conn.cursor())
            session["user_id"] = user.user_ID  
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials", 401
    return render_template("signin.html")
        

@app.route("/signout")
def signout():
    session.pop("user_id", None)
    return redirect(url_for("signin"))

@app.route("/account")
def account():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = db.get_user_by_id(session['user_id'], conn.cursor())
    return render_template("account.html", user=user)

@app.route("/update_account")
def update_account():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        authenticator.save_user_data(email, password)
        db.updateuser(email, password)
        return redirect(url_for("account"))
    return render_template("update_account.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        results = db.search_posts(query, conn.cursor())
        return render_template("search_results.html", results=results)
    return render_template("search.html")

@app.route("/view_post/<int:post_id>", methods=["GET"])
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
    
    

@app.route("/post") 
def post():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        newThread = Thread(session['user_id'], title, content)
        db.create_post(session['user_id'], title, content, conn.cursor())
        return redirect(url_for("dashboard"))
    return render_template("create_post.html")


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
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
