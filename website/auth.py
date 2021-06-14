from flask import Blueprint, request, redirect, render_template, url_for, flash
from . import read_settings, db
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint(name="auth", import_name=__name__)

settings = read_settings()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash(
                    f"Logged In Successfully as {user.email}!", category="success")
                return redirect(url_for("views.home"))

    return render_template("login.html", settings=settings, user=current_user)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email Already Exists", category="error")

        elif len(password) < 8:
            flash("Too short password", category="error")

        elif confirm_password != password:
            flash("Passwords does not match", category="error")

        else:
            entry = User(email=email, username=username, password=generate_password_hash(
                confirm_password, method="sha256"))
            db.session.add(entry)
            db.session.commit()

            login_user(user, remember=True)

            flash(
                "Account created!",
                category="success"
            )

            return redirect(url_for("views.home"))

    return render_template("register.html", settings=settings, user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
