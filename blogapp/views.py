from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from .models import BlogPost, User, Releases
from .forms import RequestResetForm, ResetPasswordForm
from .utils import send_reset_email

views = Blueprint("views", __name__)

@views.route('/home')
@views.route("/")
def home():
	return render_template("index.html")


@views.route("/blog")
def blog():
	page = request.args.get("page", 1, type=int)
	posts =  BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(per_page=5, page=page)
	return render_template("blog.html", title="Blog", posts=posts)

@views.route("/about")
def about():
	return render_template("about.html", title="About")

@views.route("/message")
def message():
	return render_template("message.html", title="Message")


@views.route("/post/<int:post_id>")
def post(post_id):
    post =  BlogPost.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)



@views.route("/releases")
def releases():
	post_category = request.args.get("category", 1)
	if post_category=="All" or post_category==1:
		posts = Releases.query.all()
		return render_template("releases.html", title="Releases", posts=posts)
	else:
		posts = Releases.query.filter_by(type=post_category).all()
		return render_template("releases.html", title="Releases", posts=posts)


@views.route("/post/<string:username>")
def user_posts(username):
	page = request.args.get("page", 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts =  BlogPost.query.filter_by(author=user).order_by(BlogPost.date_posted.desc()).paginate(per_page=5, page=page)
	return render_template("user_posts.html", title="Blog", posts=posts, user=user)


@views.route("/reset_password", methods=["GET", "POST"])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash(f"An email has been sent to {form.email.data} with instructions to reset your password", "success")
		return redirect(url_for("auth.login"))
	return render_template("reset_request.html", title="Reset Password", form=form)


@views.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for("views.home"))
	user = User.verify_reset_token(token)
	if not user:
		flash("Token has expired or is invalid", "warning")
		return redirect(url_for("views.reset_request"))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data)
		user.password = hashed_password
		user.update()
		flash(f"Your password has been updated! You are now able to log in { user.username }", "success")
		return redirect(url_for("auth.login"))
	return render_template("reset_password.html", title="Reset Password", form=form)
	