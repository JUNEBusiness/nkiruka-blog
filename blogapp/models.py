from .extensions import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Interger, primary_key=True)
    username = db.column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.string(120), unique=True, nullable=False)
    image_file = db.column(db.text, nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('BlogPosts', backref = "Author", lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User %r>" % self.id
    

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    title = db.column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nulable=False, default= datetime.utcnow)
    user_id = db.column(db.Integer, db.ForeignKey("user.id"), nullable=False)


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<BlogPost %r>" % self.id
    

class Releases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.string(120), nullable=False)
    title = db.column(db.string(120), unique=True, nullable=False)
    date = db.Column(db.string(120), nullable=False)
    date_posted = db.Column(db.DateTime, nulable=False, default= datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return "<Releases %r>" % self.id