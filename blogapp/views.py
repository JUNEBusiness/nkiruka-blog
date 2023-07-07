from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from .models import BlogPost, User, Releases

views = Blueprint("views", __name__)

@views.route('/home')
@views.route("/")
def home():
	return render_template("index.html")


@views.route("/blog")
def blog():
	posts =  BlogPost.query.all()
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
	post_category = request.args.get("category").strip().capitalize()
	if post_category=="All" or post_category==1:
		posts = Releases.query.all()
		return render_template("releases.html", title="Releases", posts=posts)
	else:
		posts = Releases.query.filter_by(type=post_category).all()
		return render_template("releases.html", title="Releases", posts=posts)


