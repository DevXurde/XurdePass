from flask import Blueprint

auth = Blueprint(name="auth", import_name=__name__)


@auth.route("/login")
def login():
    return "This is Login Page"


@auth.route("/register")
def register():
    return "This is register page."


@auth.route("/logout")
def logout():
    return "This is Logout Page"
