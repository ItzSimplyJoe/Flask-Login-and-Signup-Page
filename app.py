from flask import Flask, render_template, request, redirect, url_for, flash
from static.database.databases import db

app = Flask("ItzSimplyJoe")
app.secret_key = 'superawesomesecretkey1010001'


@app.route("/")
def home():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/forgotten_password')
def forgotten_password():
    return render_template("forgotten_password.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route("/createaccount", methods=["POST"])
def create_account():
    username = request.form["username"]
    password = request.form["password"]
    others = db.fetch(username)
    if others != []:
        flash("Username already exists", "error")
        return redirect(url_for("signup"))
    else:
        if len(password) < 8:
            flash("Password must be at least 8 characters long", "error")
            return redirect(url_for("signup"))
        else:
            try:
                db.insert(username, password)
                flash("Account created successfully, please login", "success")
                return redirect(url_for("signup"))
            except:
                flash("An error occured", "error")
                return redirect(url_for("signup"))

@app.route("/login_account", methods=["POST"])
def login_account():
    username = request.form["username"]
    password = request.form["password"]
    user = db.login(username, password)
    if user:
        return redirect(url_for("success"))
    else:
        flash ("Incorrect username or password", "error")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)