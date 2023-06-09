from flask import Blueprint, render_template, redirect, url_for
from .forms import RegistrationForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route("/profile", methods=["GET", "POST"])
def profile():
    pass


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    pass


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Register", form=form)


@auth.route("/post", methods=["GET", "POST"])
def post():
    pass