from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date
from enum import Enum

class Usertype(Enum):
    ADMIN = 0, 'Administrator'
    FREE = 1, 'Free account'
    BASIC = 2, 'Basic account'
    PREMIUM = 3, 'Premium account'
    def __int__(self):
        return self.value[0]
    def __str__(self):
        return self.value[1]


class Visibility(Enum):
    NONE = 0, 'None'
    FRIENDS = 1, 'Only friends'
    ALL = 2, 'All'
    def __int__(self):
        return self.value[0]
    def __str__(self):
        return self.value[1]


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author= db.Column(db.String(50))
    publisher= db.Column(db.String(50))
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    size = db.Column(db.Integer)
    visibility = db.Column(db.Integer, nullable=False, default=int(Visibility.NONE))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password= db.Column(db.Text, nullable=False)
    email= db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    login_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    name= db.Column(db.String(20))
    surname= db.Column(db.String(50))
    type= db.Column(db.Integer, nullable=False, default=int(Usertype.FREE))
    books = db.relationship('Book')
    friends = db.relationship('Friend', foreign_keys="Friend.user_id")


class Friend(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)



