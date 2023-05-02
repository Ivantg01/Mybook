#### Imports
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Book
import datetime
from . import db
import json
from fileinput import filename
from gconfig import gconfig
import ebooklib
from ebooklib import epub
import os #for file_stats, path
import shutil #for move files
import tempfile #for read_book
from gconfig import gconfig

#### Variables
views = Blueprint('views', __name__)

#### Display the home page of the web
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

#### Display the list of books of the current user
@views.route('/catalog', methods=['GET', 'POST'])
@login_required
def catalog():
    sort = request.args.get('sort')
    reverse = request.args.get('reverse')
    return render_template("catalog.html", user=current_user, sort=sort, reverse=reverse)

#### Display the books of the current user in a table with the covers
@views.route('/bookshelf', methods=['GET', 'POST'])
@login_required
def bookshelf():
    return render_template("bookshelf.html", user=current_user)

#### Delete a book of the current user
@views.route('/delete-book', methods=['POST'])
def delete_book():
    book = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    book_id = book['book_id']
    book = Book.query.get(book_id)
    if book:
        if book.user_id == current_user.id:
            db.session.delete(book)
            db.session.commit()
            folder = f'{gconfig.BOOK_PATH}/b{book.id:07d}'
            shutil.rmtree(folder, ignore_errors=True) # removing directory with this book

    return jsonify({})

#### Write a file in html with the content of a book
def write_book_html(epub, folder: str, filename: str):
    #buscamos el texto de los capitulos y lo almacenamos junto al fichero epub
    sections = []
    for item in epub.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        sections.append(item)
    # Crea un archivo temporal HTML que contiene las secciones del archivo EPUB
    with open(f'{folder}/{filename}', 'wb') as f:
        for section in sections:
            f.write(section.get_content())

#### Store the uploaded file and return the file name
def store_uploaded_file (my_file) -> str:
    filename = "";
    if my_file.filename:
        #Verify that the book root folder exists
        if os.path.isdir(gconfig.BOOK_PATH) == False:
            print(f'Creamos BOOK_PATH: {gconfig.BOOK_PATH}')
            os.mkdir(gconfig.BOOK_PATH)  #create main folder for epubs
        filename = os.path.join(gconfig.BOOK_PATH, my_file.filename)
        my_file.save(filename)
    return filename

### Extract all images from an epub and stores in the book folder
### images have the same name than the epub with a letter: b0000000a.jpg, b0000000b.jpg, ...
def extract_and_store_images (epub, folder: str, book_id: int):
    ch='a'
    for item in epub.get_items_of_type(ebooklib.ITEM_IMAGE):
        with open(f'{folder}/b{book_id:07d}{ch}.jpg', 'wb') as f:
            f.write(item.get_content())
        ch = chr(ord(ch) + 1)

### Get the title of a book from the metadata
def get_epub_metadata_title (epub) -> str:
    title = ""
    if (len(epub.get_metadata('DC', 'title')) > 0):
        title = epub.get_metadata('DC', 'title')[0][0]
    return title

### Get the author of a book from the metadata
def get_epub_metadata_author (epub) -> str:
    author = ""
    if (len(epub.get_metadata('DC', 'creator')) > 0):
        author = epub.get_metadata('DC', 'creator')[0][0]
    return author

### Get the publisher of a book from the metadata
def get_epub_metadata_publisher (epub) -> str:
    publisher = ""
    if (len(epub.get_metadata('DC', 'publisher')) > 0):
        publisher = epub.get_metadata('DC', 'publisher')[0][0]
    return publisher

### Get the date of a book from the metadata
def get_epub_metadata_date (epub) -> str:
    try:
        date = datetime.datetime.strptime(epub.get_metadata('DC', 'date')[0][0],'%Y-%m-%d').date()
    except:
        date = None
    return date

#### Add a book to the current user from a epub file
@views.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        #read epub file and verify content
        f = request.files['file']
        filename = store_uploaded_file(f)
        if filename:
            flash(f'File {f.filename} uploaded', category='success')
        else:
            flash('Error uploading file', category='error')
            return render_template("add_book.html", user=current_user)
        try:
            my_epub = epub.read_epub(filename)
        except:
            flash(f'Error procesing file {f.filename}', category='error')
            os.remove(filename)  #eliminamos el fichero subido erroneo
            return render_template("add_book.html", user=current_user)

        #read the metadata of the book
        #title=None; author=None; publisher=None; date=None;
        title = get_epub_metadata_title(my_epub)
        if title:
            flash(f'Book {title} detected', category='success')
        else:
            flash('Error procesing file', category='error')
            return render_template("add_book.html", user=current_user)
        author = get_epub_metadata_author(my_epub)
        publisher = get_epub_metadata_publisher(my_epub)
        date = get_epub_metadata_date(my_epub)
        size = os.stat(filename).st_size

        #create book object and add to database
        new_book = Book(title=title, author=author, publisher=publisher, date=date, size=size,
                        user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()

        #create a new folder for the book with the book id
        folder = os.path.join(gconfig.BOOK_PATH, f'b{new_book.id:07d}')
        if os.path.isdir(folder) == False:
            os.mkdir(folder)  #create subfolder for the epub with name b9999999
        shutil.move(filename, os.path.join(folder, f'b{new_book.id:07d}.epub')) #rename book file with b9999999.epub
        flash('Book added!', category='success')

        #buscamos las imagenes y las almacenamos junto al fichero epub con sufijos a,b,c ...
        extract_and_store_images(my_epub, folder, new_book.id);
        new_book.coverfile = f'b{new_book.id:07d}/b{new_book.id:07d}a.jpg'
        db.session.commit()  #actualizamos el nombre del coverfile

        #redireccionamos a update book con GET para mostrar el nuevo libro
        return redirect(url_for('views.update_book', id=new_book.id))

    return render_template("add_book.html", user=current_user)

#### Find the file names of the images of a book
def find_book_images(book_id: int) -> list:
    images=[];
    for ordinal in range (97, 110):  #iteramos de la 'a' a la 'z'
        image_file = f'b{book_id:07d}/b{book_id:07d}{ordinal:c}.jpg'
        if os.path.isfile(os.path.join(gconfig.BOOK_PATH, image_file)):
            images.append(image_file)
        else:   #si no existe fichero paramos de buscar ya que no hay mas imagenes
            break
    return images

#### Display the information of a book and allow the current user to modify
@views.route('/update_book', methods=['GET', 'POST'])
@login_required
def update_book():
    if request.method == 'GET':     #Display the book information
        book_id = int(request.args.get('id'))
        book = Book.query.filter_by(id=book_id, user_id=current_user.id).first()
        if book is None:
            return redirect(url_for('views.catalog'))
        #buscamos las imagenes sacadas del libro
        images = find_book_images(book_id)
        return render_template("update_book.html", user=current_user, book=book, images=images)
    elif request.method == 'POST':  #Update de database with the changes of the book information
        book_id = request.form.get('id')
        title = request.form.get('title')
        author = request.form.get('author')
        publisher = request.form.get('publisher')
        try:
            date = datetime.datetime.strptime(request.form['date'],'%Y-%m-%d').date()
        except:
            date = None
        coverfile = request.form.get('image')

        book = Book.query.filter_by(id=book_id, user_id=current_user.id).first()
        if book: #update information of the book
            book.title=title;
            book.author=author;
            book.publisher=publisher;
            book.date=date;
            book.coverfile=coverfile;
            db.session.commit()
            flash('Book data updated!', category='success')
            return redirect(url_for('views.catalog'))

    return render_template("update_book.html", user=current_user, book=book)

#### Display the table of contents (TOC) of a book and add the content in each chapter of the TOC
from .tools import parse_book_toc
@views.route('/read_book', methods=['GET', 'POST'])
@login_required
def read_book():

    book_id = int(request.args.get('id'))
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first()

    if (book):
        # Abre el EPUB y crea una lista de las secciones del archivo EPUB: chapter link: chapter name
        ebook = epub.read_epub(f'{gconfig.BOOK_PATH}/b{book_id:07d}/b{book_id:07d}.epub')
        toc = parse_book_toc(ebook.toc)

        #obtenemos el contenido de los capitulos a partir del TOC
        chapters= {}
        for chapter_link, chapter_name  in toc.items():
            chapter_link =  chapter_link.split('#')[0]  #remove chapter link suffix after '#'
            chapters[chapter_name] = ebook.get_item_with_href(chapter_link).get_content().decode('utf-8')

        # Renderiza el archivo HTML en la plantilla
        return render_template("read_book.html", user=current_user, book=book, chapters=chapters)
    return redirect(url_for('views.catalog'))


