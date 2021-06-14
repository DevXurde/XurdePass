from flask import Blueprint, render_template, request, flash, redirect
from flask.helpers import url_for
from . import read_settings, db
from .models import Password
from flask_login import login_required, current_user

views = Blueprint(name="views", import_name=__name__)

settings = read_settings()


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        url = request.form.get("url")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            entry = Password(url=url, username=username, email=email,
                             password=password, user_id=current_user.id)
            db.session.add(entry)
            db.session.commit()

        except:
            flash("Could'nt save password", category="error")

    data = Password.query.order_by(Password.id).all()
    return render_template("index.html", settings=settings, user=current_user, data=data)


@views.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    data = Password.query.filter_by(id=id)

    if request.method == "POST":
        url = request.form.get("url")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            data.update(dict(
                url=url,
                username=username,
                email=email,
                password=password
            ))
            db.session.commit()
            flash("Password Updated", category="success")
            return redirect(url_for("views.home"))

        except:
            flash("Could'nt update password", category="error")
            return redirect(url_for("views.home"))

    return render_template("edit.html", settings=settings, user=current_user, data=data.first())


@views.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    try:
        password = Password.query.filter_by(id=id).first()
        db.session.delete(password)
        db.session.commit()
        flash("Deleted Password", category="success")
        return redirect(url_for("views.home"))

    except:
        flash("Could'nt delete password", category="error")
        return redirect(url_for("views.home"))
