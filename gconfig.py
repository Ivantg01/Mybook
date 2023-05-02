####imports
from decouple import config

####variables
class gconfig:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///mybooks.db"
    DEBUG = False
    BOOK_FOLDER_NAME = "bookfiles"
    BOOK_PATH = "" # booksubfolder and the website will be in the same directory

#####function to read .env file with program configuration
def read_dot_env_configuration():
    gconfig.SECRET_KEY = config('SECRET_KEY', default=gconfig.SECRET_KEY)
    gconfig.SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI', default=gconfig.SQLALCHEMY_DATABASE_URI)
    gconfig.DEBUG = config('DEBUG', default=gconfig.DEBUG, cast=bool)
    gconfig.BOOK_FOLDER_NAME = config('BOOK_FOLDER_NAME', default=gconfig.BOOK_FOLDER_NAME)


