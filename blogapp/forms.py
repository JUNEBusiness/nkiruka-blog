from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email =  StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7, max=100)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7, max=100)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ReleasesForm(FlaskForm):
    title =  StringField("Title", validators=[DataRequired(), Length(min=2, max=50)])
    type =  StringField("Type", validators=[DataRequired(), Length(min=2, max=20)])
    date =  DateField("Date", validators=[DataRequired()])


class Account(FlaskForm):
    title =  StringField("Email", validators=[DataRequired(), Length(min=2, max=50)])
    content =  StringField("Email", validators=[DataRequired()])


class BlogPostForm(FlaskForm):
    title =  StringField("Email", validators=[DataRequired(), Length(min=2, max=50)])
    content =  StringField("Email", validators=[DataRequired()])

