from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
@app.route("/")
def hello(name=None):
    return render_template('base_post.html', person=name)