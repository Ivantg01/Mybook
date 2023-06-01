# Mybook
Gestor online de libros electronicos multiusuario y lector ePub

## Instalación
Funcionando sobre python 3.9

```bash
pip install Flask
pip install Flask-SQLAlchemy
pip install flask-login
pip install EbookLib
pip install python-decouple
```

Para ejecutarlo desde linea de comandos Windows (con debug activado y acceso local):
```bash
set FLASK_APP=main
set FLASK_DEBUG=True
python -m flask run
```
Para ejecutarlo desde linea de comandos Linux (con debug activado y acceso local):
```bash
export FLASK_APP=main.py
export FLASK_DEBUG=True
python3 -m flask run
```
## Acceder al servidor web
Abrir la página web `http://127.0.0.1:5000`

## Base de datos
Funciona con base de datos ___sqllite___ que se almacena localmente en _venv->var->website->website-instance->mybooks.db_

La base de datos se crea automaticamente desde dentro del programa.

Las tablas definidas en el fichero ___models.py___ son:
* Tabla ___User___ contiene los datos de los usuarios 
* Tabla ___Book___ contiene loslos datos de los libros
* Tabla ___Friend___ contiene las relaciones de amistad entre usuarios

La base de datos ___sqllite___ se puede consultar arrastrando el fichero **mybooks.db** a webs online como: https://sqliteviewer.app
o utilizar programas como https://portableapps.com/apps/development/sqlite_database_browser_portable

## Entorno
Funciona con un fichero ___.env___ para almacenar las variables de entorno principales.
Consultar como ejemplo el fichero _.env.example_ con las variables a definir esperadas


## Créditos

* Sobre todo: https://github.com/techwithtim/Flask-Web-App-Tutorial video https://www.youtube.com/watch?v=dam0GPOAvVI
* En menor medida: https://github.com/alexroel/blog-flask video https://www.youtube.com/watch?app=desktop&v=JTAY5_LO0Ug
* Libros en formato epub de dominio público: https://www.elejandria.com/

## Screenshots
<img src="./screenshots/01%20Home.png" width="30%"></img>
<img src="./screenshots/02 Sign Up.png" width="30%"></img>
<img src="./screenshots/03 Add book load.png" width="30%"></img>
<img src="./screenshots/04 Add book confirm.png" width="30%"></img>
<img src="./screenshots/05 Catalog.png" width="30%"></img>
<img src="./screenshots/06 Bookshelf.png" width="30%"></img>
<img src="./screenshots/08 Read book.png" width="30%"></img>
<img src="./screenshots/09 Update user profile.png" width="30%"></img>
<img src="./screenshots/10 Administration.png" width="30%"></img>
