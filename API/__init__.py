from flask import Flask
from .product.crud import crud_namespace
from flask_restx import Api
from .config import config_dict
from .utils import db
from .model import Products
from flask_migrate import Migrate




def create_app(config=config_dict['test']):
    app= Flask(__name__)
    app.config.from_object(config_dict[config])
    db.init_app(app)
    migrate=Migrate(app,db)
    api=Api(app)
    api.add_namespace(crud_namespace, path="/")


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "products":Products
        }
    return app
