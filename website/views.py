from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Book
import datetime
from . import db
import json

views = Blueprint('views', __name__)

from pprint import pprint


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        publisher = request.form.get('publisher')
        date = request.form.get('date')

        if len(title) < 1:
            flash('Tittle is too short!', category='error')
        else:
            new_book = Book(title=title, user_id=current_user.id, author=author, publisher=publisher, date=date)  #providing the schema for the book
            db.session.add(new_book) #adding the book to the database
            db.session.commit()
            flash('Book added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-book', methods=['POST'])
def delete_book():
    book = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    book_id = book['book_id']
    book = Book.query.get(book_id)
    if book:
        if book.user_id == current_user.id:
            db.session.delete(book)
            db.session.commit()

    return jsonify({})

@views.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        publisher = request.form.get('publisher')
        try:
            date = datetime.datetime.strptime(request.form['date'],'%Y-%m-%d').date()
        except:
            date = None

        book = Book.query.filter_by(title=title).first()
        if book:
            flash(f'Book title already exists: {title}.', category='error')
        elif len(title) < 3:
            flash('Book title must be greater than 3 characters.', category='error')
        else:
            new_book = Book(title=title, author=author, publisher=publisher, date=date,
                            user_id=current_user.id)
            db.session.add(new_book)
            db.session.commit()
            flash('Book created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("add_book.html", user=current_user)

