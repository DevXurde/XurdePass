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
        remember_me = str(request.form.get("remember_me"))

        print(remember_me)

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                if remember_me == "on":
                    login_user(user, remember=True)
                else:
                    login_user(user, remember=False)

                flash(
                    f"Hello {user.username} !", category="success")
                return redirect(url_for("dashboard.manager"))

            else:
                flash(f"Incorrect password for {user.email}", category="error")
                return redirect(url_for("auth.login"))

        else:
            flash(f"Email does not exists", category="error")
            return redirect(url_for("auth.login"))

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

            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)

            flash(
                "Account created!",
                category="success"
            )

            return redirect(url_for("dashboard.manager"))

    return render_template("register.html", settings=settings, user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard.manager"))
