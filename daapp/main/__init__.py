from flask import Flask, Blueprint
from flask_restplus import Api

from daapp.main.config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    from mlapp.main.router.ml_routes import ns_ml
    api_blueprint = Blueprint('analysis_api', __name__)
    api = Api(api_blueprint,
              title='Analysis API',
              version=1.0,
              description='A RESTful web service for Machine Learning services')
    api.add_namespace(ns_ml, path='/')
    app.register_blueprint(api_blueprint, url_prefix='/analysis/v1')

    return app
