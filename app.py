from flask import Flask, session, request, url_for, redirect, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # TODO: Actually login/register
        if 'form' in request.form:
            return 'Invalid request.'
        elif request.form['type'] == 'login':
            return 'Login functionality <em>coming soon!</em>'
        elif request.form['type'] == 'register':
            return 'Register functionality <em>coming soon!</em>'
    return render_template('welcome.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
