from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash


from .forms import RegistrationForm, LoginForm
from .models import User, BlogPost, Releases

auth = Blueprint("auth", __name__)

@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    pass


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", title="Login", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            print("Hello! something is wrong if you do not get a bounceback!")
            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash("You have been logged in successfully!", "success")
                return redirect(url_for("views.home"))
            else:
              flash("There is no user with these credentials in our database!", "danger")
              return redirect(url_for("auth.login"))
        else:
            flash("Incorrect email or password!", "danger")
            return render_template("login.html", title="Login", form=form)


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("register.html", title="Register", form=form)
    elif request.method =="POST":
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
            user.insert()
            flash(f"Your account has been created! You are now able to log in { form.username.data }", "success")
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return render_template("register.html", title="Register", form=form)



@auth.route("/post", methods=["GET", "POST"])
@login_required
def post():
    return render_template("post.html", title="Post")