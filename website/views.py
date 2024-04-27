from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Receipt, User
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home ():
    all_data = Receipt.query.all()
    profile = User.query.all()
    return render_template("home.html", user = current_user, nota = all_data, profile_user=profile)


