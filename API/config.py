import os
from decouple import config



BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_kEY = config("SECRET_KEY",'secret')
    SQLALCHEMY_TRACKMODIFICATIONS =False

class DevConfig(Config):
    DEBUG=config('DEBUG',default =False, cast=bool)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIRECTORY,'db.sqlite3')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Prod(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # postgresql://database_8ss6_user:42Vv2cC3Zmi6trpaMNTTqx4wL3umJBF8@dpg-csc7ol88fa8c73fqqmag-a.oregon-postgres.render.com/database_8ss6
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG=config('DEBUG', cast=bool)
BASE_DIRECTORY


config_dict ={
    'dev':DevConfig,
    'test':TestConfig,
    'prod':Prod
}
