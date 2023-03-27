from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Book
import datetime
from . import db
import json
from fileinput import filename
import ebooklib
from ebooklib import epub
import os #for file_stats
import shutil #for move files
import tempfile #for read_book

views = Blueprint('views', __name__)

from pprint import pprint


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/catalog', methods=['GET', 'POST'])
@login_required
def catalog():
    return render_template("catalog.html", user=current_user)

@views.route('/bookshelf', methods=['GET', 'POST'])
@login_required
def bookshelf():
    return render_template("bookshelf.html", user=current_user)

@views.route('/delete-book', methods=['POST'])
def delete_book():
    book = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    book_id = book['book_id']
    book = Book.query.get(book_id)
    if book:
        if book.user_id == current_user.id:
            db.session.delete(book)
            db.session.commit()
            folder = f'bookfiles/b{book_id:07d}'
            shutil.rmtree(folder, ignore_errors=True) # removing directory with this book

    return jsonify({})

@views.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        #read epub file and verify content
        f = request.files['file']
        if f.filename:
            flash(f'File {f.filename} uploaded', category='success')
        else:
            flash('Error uploading file', category='error')
            return render_template("add_book.html", user=current_user)
        folder = 'bookfiles'
        if os.path.isdir(folder) == False:
            os.mkdir(folder)  #create main folder for epubs
        filename='bookfiles/'+f.filename
        f.save(filename)
        try:
            my_epub = epub.read_epub(filename)
        except:
            flash(f'Error procesing file {f.filename}', category='error')
            os.remove(filename)  #eliminamos el fichero subido erroneo
            return render_template("add_book.html", user=current_user)

        title=None; author=None; publisher=None; date=None;
        if (len(my_epub.get_metadata('DC', 'title')) > 0):
            title = my_epub.get_metadata('DC', 'title')[0][0]
        if title:
            flash(f'Book {title} detected', category='success')
        else:
            flash('Error procesing file', category='error')
            return render_template("add_book.html", user=current_user)
        if (len(my_epub.get_metadata('DC', 'creator')) > 0):
            author = my_epub.get_metadata('DC', 'creator')[0][0]
        if (len(my_epub.get_metadata('DC', 'publisher')) > 0):
            publisher = my_epub.get_metadata('DC', 'publisher')[0][0]
        size = os.stat(filename).st_size
        try:
            date = datetime.datetime.strptime(my_epub.get_metadata('DC', 'date')[0][0],'%Y-%m-%d').date()
        except:
            date = None

        #create book object and add to database
        new_book = Book(title=title, author=author, publisher=publisher, date=date, size=size,
                        user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        #print (f'id={new_book.id} title={title} author={author} pub={publisher} date={date} size={size}')
        folder = f'bookfiles/b{new_book.id:07d}'
        if os.path.isdir(folder) == False:
            os.mkdir(folder)  #create subfolder for the epub with name b9999999
        shutil.move(filename, f'{folder}/b{new_book.id:07d}.epub') #rename book file with b9999999.epub
        flash('Book added!', category='success')

        #buscamos las imagenes y las almacenamos junto al fichero epub con sufijos a,b,c ...
        ch='a'
        for a in my_epub.get_items_of_type(ebooklib.ITEM_IMAGE):
            with open(f'{folder}/b{new_book.id:07d}{ch}.jpg', 'wb') as f:
                f.write(a.get_content())
            ch = chr(ord(ch) + 1)
        new_book.coverfile = f'{folder}/b{new_book.id:07d}a.jpg'
        db.session.commit()  #actualizamos el nombre del coverfile

        #buscamos el texto de los capitulos y lo almacenamos junto al fichero epub
        sections = []
        for item in my_epub.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            sections.append(item)
        # Crea un archivo temporal HTML que contiene las secciones del archivo EPUB
        with open(f'{folder}/b{new_book.id:07d}.html', 'wb') as f:
            for section in sections:
                f.write(section.get_content())

        #redireccionamos a update book con GET para mostrar el nuevo libro
        return redirect(url_for('views.update_book', id=new_book.id))

    return render_template("add_book.html", user=current_user)

@views.route('/update_book', methods=['GET', 'POST'])
@login_required
def update_book():
    if request.method == 'GET':     #mostramos el libro ID y permitimos cambios
        id = int(request.args.get('id'))
        book = Book.query.filter_by(id=id, user_id=current_user.id).first()
        #buscamos las imagenes sacadas del libro
        if book is None:
            return redirect(url_for('views.catalog'))
        images=[];
        for ordinal in range (97, 110):  #iteramos de la 'a' a la 'z'
            image_file = f'bookfiles/b{id:07d}/b{id:07d}{ordinal:c}.jpg'
            if os.path.isfile(image_file):
                images.append(image_file)
            else:   #si no existe fichero paramos de buscar ya que no hay mas imagenes
                break
        kb= int(book.size/1000);
        return render_template("update_book.html", user=current_user, book=book, images=images, kb=kb)
    elif request.method == 'POST':  #procesamos cambios del libro ID y actualizamos base de datos
        id = request.form.get('id')
        title = request.form.get('title')
        author = request.form.get('author')
        publisher = request.form.get('publisher')
        try:
            date = datetime.datetime.strptime(request.form['date'],'%Y-%m-%d').date()
        except:
            date = None
        coverfile = request.form.get('image')

        book = Book.query.filter_by(id=id, user_id=current_user.id).first()
        if book: #actualizamos base de datos
            book.title=title;
            book.author=author;
            book.publisher=publisher;
            book.date=date;
            book.coverfile=coverfile;
            db.session.commit()
            flash('Book data updated!', category='success')
            return redirect(url_for('views.catalog'))

    return render_template("update_book.html", user=current_user, book=book)

from .tools import parse_book_toc
@views.route('/read_book', methods=['GET', 'POST'])
@login_required
def read_book():

    id = int(request.args.get('id'))
    book = Book.query.filter_by(id=id, user_id=current_user.id).first()

    # Ruta al archivo EPUB
    filename = f'bookfiles/b{id:07d}/b{id:07d}'

    # Abre el archivo EPUB
    book = epub.read_epub(filename+'.epub')
    # Crea una lista de las secciones del archivo EPUB
    chapters = parse_book_toc(book.toc)
    chapters = {} #disable chapters

    # open the html file with the content of the epub
    with open(filename+'.html', encoding="utf8") as f:
        content = f.read()

    # Renderiza el archivo HTML en la plantilla
    return render_template("read_book.html", user=current_user, book=book, chapters=chapters,
                           content = content)

#defines the book folder path associated to a book_id to store epub files
#all books are stored bookfiles folder. Each book has its own subfolder with the format bXXXXXXX
def path_of_book(book_id) :
    return f'bookfiles/b{book_id:07d}/'

