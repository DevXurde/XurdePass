from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import json

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
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from . import models
    create_db(app=app)

    return app


def create_db(app):
    if not os.path.exists(os.path.join("website", "db", db_name)):
        db.create_all(app=app)
        print("DB Created Successfully")
