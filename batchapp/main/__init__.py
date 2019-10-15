from flask import Flask, Blueprint
from flask_restplus import Api

from batchapp.main.config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    from batchapp.main.router.batch_routes import ns_batch
    api_blueprint = Blueprint('batch_api', __name__)
    api = Api(api_blueprint,
              title='Batch Application API',
              version=1.0,
              description='A RESTful web service for batch processes')
    api.add_namespace(ns_batch, path='/')
    app.register_blueprint(api_blueprint, url_prefix='/batch_api/v1')

    return app
