from unicodedata import name

from flask import Flask, render_template, request, redirect, url_for, session
import database.py, authenticator.py
app = Flask(__name__)

db = database.access_database()
conn = db.connect()

def login():
    return "Login successful."


@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template(
        'dashboard.html', 
        username=session['username'],
        role=session['role']
    )

@app.route("/")
def index(name=None):
    return render_template('base_post.html', person=name)

@app.route("/search", methods=["GET", "POST"])
def search():

@app.route("/signup")
def signup():

@app.route("/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        authenticator = authenticator.authenticate(email, password)
        if authenticator:
            return redirect(url_for("dashboard"))
        else:
            return render_template("signin.html")
        

@app.route("/signout")
def signout():

@app.route("/account")
def account():

@app.route("/update_account")
def update_account():

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