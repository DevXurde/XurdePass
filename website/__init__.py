from flask import Flask, redirect, url_for, flash
import os
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import LoginManager

db_name = "database.db"
db = SQLAlchemy()


def read_settings():
    with open("settings.json", "r") as settings:
        data = json.load(settings)
        return data


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wdwdlw wkdwkdn"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"

    db.init_app(app=app)

    from .views import views
    from .auth import auth
    from .dashboard import dashboard
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(dashboard, url_prefix="/")

    from .models import User, Password
    create_db(app=app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def to_login():
        flash("Login To Access Dashboard", category="success")
        return redirect(url_for("auth.login"))

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


def create_db(app):
    if not os.path.exists(os.path.join("website", db_name)):
        db.create_all(app=app)
        print("DB Created Successfully")
