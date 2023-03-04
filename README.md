# Mybook
Gestor online de libros electronicos multiusuario y lector ePub

## Instalación
Funcionando sobre python 3.9

```bash
pip install Flask
pip install Flask-SQLAlchemy
pip install flask-login
```

Para ejecutarlo desde linea de comandos (host 0.0.0.0 para acceder desde fuera del PC local):
```bash
set FLASK_APP=main
python -m flask run --host=0.0.0.0 --debug
```
## Acceder al servidor web
Abrir la página web `http://127.0.0.1:5000`

## Base de datos
Funciona con base de datos sqllite que se almacena localmente en venv->var->website->website-instance->mybooks.db

La base de datos se crea automaticamente desde dentro del programa

Las tablas de User para almacenar los usuarios registrados y Book para registrar los libros se definen en models.py

La base de datos sqllite se puede consultar arrastrando el fichero a webs online como: https://sqliteviewer.app
o utilizar programas como https://portableapps.com/apps/development/sqlite_database_browser_portable

## Estilos
La plantilla base carga los estilos y los iconos de bootstrap. Bootstrap permite hacer facilmente botones, menus,
mensajes, tarjetas, tablas, etc. La documentacion está en:
https://getbootstrap.com/docs/5.3/getting-started/introduction/

## Créditos

* Sobre todo: https://github.com/techwithtim/Flask-Web-App-Tutorial video https://www.youtube.com/watch?v=dam0GPOAvVI
* En menor medida: https://github.com/alexroel/blog-flask video https://www.youtube.com/watch?app=desktop&v=JTAY5_LO0Ug
