from flask import Flask, Blueprint
from flask_restplus import Api


from mlapp.main.config import config_by_name

try:
    from flask.ext.cors import CORS  # The typical way to import flask-cors
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import CORS

Cor = CORS


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    from mlapp.main.router.ml_routes import ns_ml
    api_blueprint = Blueprint('ml_api', __name__)
    api = Api(api_blueprint,
              title='Machine Learning Application API',
              version=1.0,
              description='A RESTful web service for Machine Learning services')
    api.add_namespace(ns_ml, path='/')
    app.register_blueprint(api_blueprint, url_prefix='/ml_api/v1')

    return app
