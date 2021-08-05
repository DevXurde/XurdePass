from flask import Blueprint, render_template, request, flash, redirect
from flask.helpers import url_for
from . import read_settings, db
from .models import Password
from flask_login import login_required, current_user

dashboard = Blueprint(name="dashboard", import_name=__name__)

settings = read_settings()


@dashboard.route("/dashboard", methods=["GET", "POST"])
@login_required
def manager():
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

            flash("Saved password", category="success")
            return redirect(url_for("dashboard.manager"))

        except:
            flash("Could'nt save password", category="error")
            return redirect(url_for("dashboard.manager"))

    return render_template("dashboard.html", settings=settings, user=current_user)


@dashboard.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    data = Password.query.filter_by(id=id)

    if request.method == "POST":
        url = request.form.get("url")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if data.first().user_id == current_user.id:

            try:
                data.update(dict(
                    url=url,
                    username=username,
                    email=email,
                    password=password
                ))
                db.session.commit()
                flash("Password updated", category="success")
                return redirect(url_for("dashboard.manager"))

            except:
                flash("Could'nt update password", category="error")
                return redirect(url_for("dashboard.manager"))
        else:
            return redirect(url_for("views.home"))

    return render_template("edit.html", settings=settings, user=current_user, data=data.first())


@dashboard.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    password = Password.query.filter_by(id=id).first()

    if password.user_id == current_user.id:

        try:
            db.session.delete(password)
            db.session.commit()
            flash("Password deleted", category="success")
            return redirect(url_for("dashboard.manager"))

        except:
            flash("Could'nt delete password", category="error")
            return redirect(url_for("dashboard.manager"))

    else:
        return redirect("views.home")