from unicodedata import name

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
        authenticator.save_user_data(email, username, password)
        return redirect(url_for("signin"))

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

@app.route("/rep_user")
def rep_user():

@app.route("/del_user")
def del_user():

@app.route("/view_post")
def view_post():  

@app.route("/post") 
def post():

@app.route("/del_post")
def del_post():

@app.route("/rep_post")
def rep_post():

@app.route("/edit_post")
def edit_post():

@app.route("/lock_post")
def lock_post():

@app.route("/view_thread")
def view_thread():

@app.route("/thread")
def thread():

@app.route("/del_thread")
def del_thread():

@app.route("/rep_thread")
def rep_thread():

@app.route("/edit_thread")
def edit_thread():

@app.route("/lock_thread")
def lock_thread():