####imports
from decouple import config as decouple_config

####variables
class config:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///mybooks.db"
    DEBUG = False
    BOOK_FOLDER_NAME = "bookfiles"
    BOOK_PATH = "" # booksubfolder and the website will be in the same directory

#####function to read .env file with program configuration
def read_dot_env_configuration():
    config.SECRET_KEY = decouple_config('SECRET_KEY', default=config.SECRET_KEY)
    config.SQLALCHEMY_DATABASE_URI = decouple_config('DATABASE_URL', default=config.SQLALCHEMY_DATABASE_URI)
    config.DEBUG = decouple_config('DEBUG', default=config.DEBUG, cast=bool)
    config.BOOK_FOLDER_NAME = decouple_config('BOOK_FOLDER_NAME', default=config.BOOK_FOLDER_NAME)

    if config.DEBUG:
        print (f"-----")
        print (f"config {config.SECRET_KEY=}")
        print (f"config {config.SQLALCHEMY_DATABASE_URI=}")
        print (f"config {config.DEBUG=}")
        print (f"config {config.BOOK_FOLDER_NAME=}")
        print (f"-----")

