from flask import Flask, render_template

app = Flask(__name__)
=

@app.route('/test')
def testpost():
    return render_template("testpost.html")

if __name__ == '__main__':
    app.run()
