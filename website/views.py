from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Company, User
from . import db
import json
from .scraper import get_news, get_reviews

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
	startups = Company.query.all()
	return render_template("home.html", user=current_user, startups=startups)

@views.route('/profile')
@login_required
def profile():
	return render_template("index.html")

@views.route('/startup-details')
@login_required
def details():
	args = request.args
	id = args.get('id')
	startup = Company.query.filter_by(id=id).first()
	news = get_news(startup.name)
	reviews = [review for review in startup.reviews.values()]
	return render_template("startup-details.html", user=current_user, startup=startup, news=news, reviews=reviews)