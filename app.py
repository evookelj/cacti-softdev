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

@app.route("/authenticate/", methods=['POST'])
def authenticate():
    print request.form.values()
    pw = request.form["password"]
    un = request.form["user"]
    em = request.form["email"]
    tp = request.form["account"]#login vs. register
    
    if tp == "Register":
        regRet = users.register(un,em,pw)#returns an error/success message
        #return render_template('login.html', message = regRet)
        
    if tp == "Login":
        text = users.login(un,em,pw)#error message
        if text == "":#if no error message, succesful go back home
            session["username"] = un
            return redirect(url_for('home'))
        #return render_template('login.html', message = text)

if __name__ == '__main__':
    app.debug = True
    app.run()
