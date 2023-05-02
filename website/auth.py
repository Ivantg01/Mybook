#### Imports
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Usertype, user_type_to_str
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql import func
import json
import shutil #for move files
from gconfig import gconfig

#### Variables
auth = Blueprint('auth', __name__)

#### Login with a user in the web
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                #update last login information in the database
                user.login_at = func.now()
                db.session.commit()
                return redirect(url_for('views.catalog'))
            else:
                flash('Invalid password.', category='error')
        else:
            flash('Invalid username.', category='error')

    return render_template("login.html", user=current_user)

#### Logout the current user from the web
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#### Display the user profile
@auth.route('/user_profile')
@login_required
def user_profile():
    return render_template("user_profile.html", user=current_user)

#### Check password
def check_password_format(password1: str, password2:str) ->bool:
    valid = True
    if password1 != password2:
        valid = False
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 3:
        valid = False
        flash('Password must be at least 3 characters.', category='error')
    return valid

#### Sign up a new user
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Login name already exists.', category='error')
        elif len(username) < 3:
            flash('Login name must be greater than 3 characters.', category='error')
        elif check_password_format(password1, password2):
            new_user = User(username=username, email=email, name=name, surname=surname,  #type=0, #to create root users
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.catalog'))

    return render_template("sign_up.html", user=current_user)

#### Update the profile of a user
@auth.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    #create a list with all types of users from the enumeration
    user_types = list(map(lambda x: x.value, Usertype._member_map_.values()))
    if request.method == 'GET':     #mostramos los datos del usuario y permitimos cambios
        user_id = int(request.args.get('id'))
        user = User.query.filter_by(id=user_id).first()
        #only the current user or the admin can chage the profile
        if user and (current_user.type == int(Usertype.ADMIN) or current_user.id == user.id):
            return render_template("update_user.html", user=current_user, usr=user, user_types=user_types)
    elif request.method == 'POST':  #procesamos cambios de los datos del usuario
        user_id = request.form.get('id')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')
        user_type = request.form.get('type')
        user = User.query.filter_by(id=user_id).first()
        #only the current user or the admin can chage the profile
        if user and (current_user.type == int(Usertype.ADMIN) or current_user.id == user.id):
            if password1:   #check password is changed
                if check_password_format(password1, password2):
                    return render_template("update_user.html", user=current_user, usr=user, user_types=user_types)
                else:
                    user.password = generate_password_hash(password1, method='sha256')
            if current_user.type == int(Usertype.ADMIN): #solo admin puede cambiar el tipo
                user.type = user_type
            user.email = email
            user.name = name
            user.surname = surname
            db.session.commit()
            flash('User profile updated!', category='success')
            if current_user.type == int(Usertype.ADMIN):
                return redirect(url_for('auth.administration'))

    return redirect(url_for('views.catalog'))

#### Display the list of users for administration
@auth.route('/administration', methods=['GET', 'POST'])
@login_required
def administration():
    #only admin can access
    if current_user.type != int(Usertype.ADMIN):
        return redirect(url_for('views.catalog'))

    if request.method == 'GET':
        sort = request.args.get('sort')
        reverse = request.args.get('reverse')
        users = User.query.order_by(User.username).all()
        return render_template("administration.html", user=current_user, users=users, sort=sort, reverse=reverse, user_type_to_str=user_type_to_str)

    return redirect(url_for('views.catalog'))

#### Delete a user with books
@auth.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    user_id = user['user_id']
    user = User.query.get(user_id)
    if user:
        if user.id != current_user.id:
            #Detele all book files
            for book in user.books:
                folder = f'{gconfig.BOOK_PATH}/b{book.id:07d}'
                shutil.rmtree(folder, ignore_errors=True) # removing directory with this book
            db.session.delete(user)  #delete the user
            db.session.commit()
            flash(f'User {user.username} deleted with {len(user.books)} books.', category='success')
        else:
            flash('Cannot remove your own user.', category='error')

    return jsonify({})
