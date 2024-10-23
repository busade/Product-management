import os
from decouple import config



BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config("SECRET_KEY",'secret')
    SQLALCHEMY_TRACKMODIFICATIONS =False

class DevConfig(Config):
    DEBUG=config('DEBUG',default =False, cast=bool)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIRECTORY,'db.sqlite3')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG=config('DEBUG', default = False, cast=bool)
BASE_DIRECTORY


config_dict ={
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig
}
