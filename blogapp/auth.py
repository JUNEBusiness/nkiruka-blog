from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash


from .forms import RegistrationForm, LoginForm, ReleasesForm, BlogPostForm, UpdateAccountForm
from .models import User, BlogPost, Releases
from .utils import save_picture, delete_picture, send_reset_email

auth = Blueprint("auth", __name__)

@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        try:
            if form.picture.data:
                print(form.picture.data)
                picture_file = save_picture(form.picture.data)
                garbage = current_user.image_file
                current_user.image_file = picture_file
                current_user.update()
                if garbage != "default.jpg":
                    delete_picture(garbage)
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.update()
            flash('Your account has been updated!', 'success')
        except:
            flash('Something went wrong!', 'danger')
        
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Account',
                           image_file=image_file, form=form)


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
                next_page = request.args.get('next')
                flash("You have been logged in successfully!", "success")
                return redirect(next_page) if next_page else redirect(url_for("views.home"))
            else:
              flash("There is no user with these credentials in our database!", "danger")
              return redirect(url_for("auth.login"))
        else:
            form.email.data=form.email.data
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
            if form.email.data in ["justiceomonigho@yahoo.com", "tchelberwrites@gmail.com", "kalunkeiruka2852@gmail.com"]:
                user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data), is_admin=True)  
            user.insert()
            flash(f"Your account has been created! You are now able to log in { form.username.data }", "success")
            return redirect(url_for("auth.login"))
        else:
            form.username.data=form.username.data
            form.email.data=form.email.data
            return render_template("register.html", title="Register", form=form)


@auth.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    blog = BlogPostForm()
    release = ReleasesForm()
    if blog.validate_on_submit():
        post = BlogPost(title=blog.title.data.strip(), content=blog.content.data, author=current_user)
        post.insert()
        flash("Blog posted successfully", "success")
        return redirect(url_for("views.blog"))
    elif release.validate_on_submit():
        post = Releases(type=release.type.data.strip().capitalize(), title=release.title.data.strip().capitalize(), date=release.date.data)
        print(post)
        post.insert()
        flash("Congratulations on your new release!!!", "success")
        return redirect(url_for("views.releases"))
    return render_template("create_post.html", title="Post",blog=blog, release=release)


@auth.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)      
    form = BlogPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.update()
        flash("Your post has been updated!", "success")
        return redirect(url_for("views.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("update_post.html", title="Update Post", form=form, post=post)


@auth.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post.delete()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("views.home"))
    