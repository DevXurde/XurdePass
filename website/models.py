from . import db
from flask_login import UserMixin


class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    passwords = db.relationship("Password")
