from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author= db.Column(db.String(50))
    publisher= db.Column(db.String(50))
    date = db.Column(db.Date)
    size = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password= db.Column(db.Text, nullable=False)
    email= db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    name= db.Column(db.String(20))
    surname= db.Column(db.String(50))
    books = db.relationship('Book')


