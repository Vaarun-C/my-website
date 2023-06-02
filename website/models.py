from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Company (db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	small_description = db.Column(db.Text(10000))
	large_description = db.Column(db.Text(10000))
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	video_link = db.Column(db.String(150))
	founders = db.Column(db.JSON(500))
	reviews = db.Column(db.JSON(1500))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))