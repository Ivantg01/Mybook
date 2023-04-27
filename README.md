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

Para ejecutarlo desde linea de comandos (host 0.0.0.0 para acceder desde fuera del PC local):
```bash
set FLASK_APP=main
python -m flask run --host=0.0.0.0 --debug
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
  
