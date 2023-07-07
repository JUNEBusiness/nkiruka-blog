from flask import Flask
from os import path

from .extensions import db
from .extensions import login_manager
from .extensions import mail

DB_NAME = "blog.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "951a6bfc24f2ce36b9e98069ccafbb8b42f1fbc5238f8ffd264290ef0ee59b3e"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    db.init_app(app=app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(auth)
    app.register_blueprint(views)
    
    from .models import User, BlogPost, Releases
    
    with app.app_context():
        create_database()

    return app


def create_database():
    if not path.exists("blogapp/" + DB_NAME):
        db.create_all()
        return 0