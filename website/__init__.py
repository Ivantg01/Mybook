#### Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from gconfig import read_dot_env_configuration, gconfig
import os

#### Variables
db = SQLAlchemy()

#### Create flask app
def create_app():
    #read .env variables
    read_dot_env_configuration()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = gconfig.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = gconfig.SQLALCHEMY_DATABASE_URI
    app.config['DEBUG'] = gconfig.DEBUG
    gconfig.BOOK_PATH = os.path.join(os.path.dirname(app.root_path), gconfig.BOOK_FOLDER_NAME)
    db.init_app(app)

    from .auth import auth
    from .views import views


    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')


    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Book
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
