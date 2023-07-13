from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField,TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User



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
    date =  DateField("Date (YYYY-MM-DD)", format='%Y-%m-%d', default=datetime.utcnow(), validators=[DataRequired()])
    submit = SubmitField("Submit")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20, message="Your username should be more than 2 characters and less than 20")])
    email =  EmailField("Email", validators=[DataRequired(), Email(message="Please input a valid email"), Length(min=6, max=40, message="Your email should be more than 6 characters and less than 40")])
    picture = FileField('Click to upload image', validators=[FileAllowed(['jpg', 'png', 'svg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != self.username.data:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                raise ValidationError("This username is taken.")
        
    
    def validate_email(self, email):
        if current_user.email != self.email.data:
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                raise ValidationError("This email is taken.")


class BlogPostForm(FlaskForm):
    title =  StringField("Title", validators=[DataRequired(), Length(min=2, max=50,  message="Your phone number should be more than 2 characters and less than 50")])
    content =  TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class RequestResetForm(FlaskForm):
    email =  EmailField("Email", validators=[DataRequired(), Email(message="Please input a valid email")])
    submit = SubmitField("Request password reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            raise ValidationError({"Response": f" A reset email has been sent to {self.email.data}"})

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7, max=100, message="Your password should be more than 7 characters and less than 100")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", "Passwords does not match!")])
    submit = SubmitField("Reset password")
