from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort, Flask
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
import os
import pathlib

from dotenv import dotenv_values

env_vars = dotenv_values()

auth = Blueprint('auth', __name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
GOOGLE_CLIENT_ID = env_vars["CLIENT_ID"]
REDIRECT_URI = 	env_vars["REDIRECT_URI"]
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
	client_secrets_file=client_secrets_file,
	scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
	redirect_uri=REDIRECT_URI
)

@auth.route("/login-google", methods=['GET', 'POST'])
def login_google():
	authorization_url, state = flow.authorization_url()
	session["state"] = state
	return redirect(authorization_url)

@auth.route("/callback", methods=['GET', 'POST'])
def callback():
	flow.fetch_token(authorization_response=request.url)

	credentials = flow.credentials
	request_session = requests.session()
	cached_session = cachecontrol.CacheControl(request_session)
	token_request = google.auth.transport.requests.Request(session=cached_session)

	id_info = id_token.verify_oauth2_token(
		id_token=credentials._id_token,
		request=token_request,
		audience=GOOGLE_CLIENT_ID
	)
	email = id_info.get("email")
	name = id_info.get("name")
	password = id_info.get("sub")

	user = User.query.filter_by(email=email).first()
	if not user:
		user = User(email=email, first_name=name, password=generate_password_hash(password, method='sha256'))
		db.session.add(user)
		db.session.commit()

	login_user(user)
	return redirect(url_for('views.home'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		data = request.form
		email = data['email']
		password = data['password']

		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Logged in successfully!', category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password, try again.', category='error')
		else:
			flash('Email does not exist.', category='error')

	return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
	if 'google_token' in session:
		try:
			id_token.verify_oauth2_token(session['google_token'], requests.Request(), session['google_id'])
			session.pop('google_token', None)
			session.pop('google_id', None)
		except ValueError:
			pass
	logout_user()
	session.clear()
	return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		data = request.form
		email = data['email']
		name = data['firstName']
		password1 = data['password1']
		password2 = data['password2']
		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exists.', category='error')
		elif len(email) < 4:
			flash('Email must be greater than 4 characters.', category='error')
		elif len(name)<2:
			flash('Name must be greater than 1 character.', category='error')
		elif len(password1) < 7:
			flash('Password must be at least 7 characters.', category='error')
		elif password1 != password2:
			flash('Passwords don\'t match.', category='error')
		else:
			new_user = User(email=email, first_name=name, password=generate_password_hash(password1, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			flash('Account created!', category='success')
			login_user(new_user, remember=True)
			return redirect(url_for('views.home'))
	return render_template("signup.html", user=current_user)