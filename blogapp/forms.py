from flask_wtf import Flaskform
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(Flaskform):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email =  StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7, max=100)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField("Sign Up")


class LoginForm(Flaskform):
    email =  StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7, max=100)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ReleasesForm(Flaskform):
    title =  StringField("Email", validators=[DataRequired(), Length(min=2, max=50)])
    type =  StringField("Email", validators=[DataRequired(), Length(min=2, max=20)])
    date =  StringField("Email", validators=[DataRequired(), Length(min=2, max=20)])


class BlogPostForm(Flaskform):
    title =  StringField("Email", validators=[DataRequired(), Length(min=2, max=50)])
    content =  StringField("Email", validators=[DataRequired()])

