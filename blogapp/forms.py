from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField,TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

from werkzeug.security import check_password_hash

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20, message="Your username should be more than 2 characters and less than 20")])
    email =  EmailField("Email", validators=[DataRequired(), Email(message="Please input a valid email"), Length(min=6, max=40, message="Your email should be more than 6 characters and less than 40")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7, max=100, message="Your password should be more than 7 characters and less than 100")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", "Passwords does not match!")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            raise ValidationError("This username is taken.")
        
    
    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            raise ValidationError("This email is taken.")



class LoginForm(FlaskForm):
    email =  EmailField("Email", validators=[DataRequired(), Email(message="Please input a valid email")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7, max=100,  message="Your password should be more than 7 characters and less than 100")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("Incorrect email.")
            return False


class ReleasesForm(FlaskForm):
    title =  StringField("Title", validators=[DataRequired(), Length(min=2, max=50,  message="Your title should be more than 2 characters and less than 50")])
    type =  StringField("Type", validators=[DataRequired(), Length(min=2, max=20,  message="Your phone number should be more than 2 characters and less than 20")])
    date =  DateTimeField("Date", validators=[DataRequired()], format= "%Y-%m-%d")


class Account(FlaskForm):
    title =  StringField("Email", validators=[DataRequired(), Length(min=2, max=50,  message="Your phone number should be more than 2 characters and less than 50")])
    content =  StringField("Email", validators=[DataRequired()])


class BlogPostForm(FlaskForm):
    title =  StringField("Email", validators=[DataRequired(), Length(min=2, max=50,  message="Your phone number should be more than 2 characters and less than 50")])
    content =  TextAreaField("Email", validators=[DataRequired()])

