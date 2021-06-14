from flask import Blueprint, render_template
from . import read_settings
from flask_login import current_user

views = Blueprint(name="views", import_name=__name__)

settings = read_settings()


@views.route("/")
def home():
    return render_template("index.html", settings=settings, user=current_user)
