from flask import Flask
from os import path

from .extensions import db

DB_NAME = "blog.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "951a6bfc24f2ce36b9e98069ccafbb8b42f1fbc5238f8ffd264290ef0ee59b3e"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB_NAME"

    db.init_app(app=app)


    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    
    from .models import User, BlogPost, Releases
    
    # with app.app_context():
    #     db.create_all()

    return app


def create_database(app):
    if not path.exists("blogapp/" + DB_NAME):
        db.create_all(app=app)
        return 0