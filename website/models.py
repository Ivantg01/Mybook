#### Imports
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date
from enum import Enum

#### Variables
class Usertype(Enum):
    ADMIN = 0, 'Administrator'
    FREE = 1, 'Free account'
    BASIC = 2, 'Basic account'
    PREMIUM = 3, 'Premium account'
    def __int__(self):
        return self.value[0]
    def __str__(self):
        return self.value[1]

def user_type_to_str(int_value):
    if int_value == 0:
        return str(Usertype.ADMIN)
    if int_value == 1:
        return str(Usertype.FREE)
    if int_value == 2:
        return str(Usertype.BASIC)
    if int_value == 3:
        return str(Usertype.PREMIUM)
    return ""

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
    coverfile = db.Column(db.String(20))
    visibility = db.Column(db.Integer, nullable=False, default=int(Visibility.NONE))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


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
    #these relations are for a quick access to books and friends of each user
    books = db.relationship('Book', backref="user", passive_deletes='all')
    friends = db.relationship('Friend', foreign_keys="Friend.user_id", passive_deletes='all')


class Friend(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    #these relations are for a quick access to friends and users attributes
    user = db.relationship('User', primaryjoin="Friend.user_id==User.id", back_populates="friends")
    friend = db.relationship('User', primaryjoin="Friend.friend_id==User.id", back_populates="friends")


