from flask import Blueprint, render_template, redirect, url_for
from forms import RegistrationForm, LoginForm

auth = Blueprint("auth", __name__)

auth.route("/account", method = ["POST", "GET"])
def account():
    pass


auth.route("/login", method = ["POST", "GET"])
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)


auth.route("/logout", method = ["POST", "GET"])
def logout():
    pass


auth.route("/register", method = ["POST", "GET"])
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Register", form=form)


auth.route("/post", method = ["POST", "GET"])
def post():
    pass