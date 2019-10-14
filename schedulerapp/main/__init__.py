from flask import Flask, Blueprint
from flask_restplus import Api

from schedulerapp.main.config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    from schedulerapp.main.router.scheduler_routes import ns_scheduler
    api_blueprint = Blueprint('scheduler_api', __name__)
    api = Api(api_blueprint,
              title='Scheduler Application API',
              version=1.0,
              description='A RESTful web service for scheduling processes')
    api.add_namespace(ns_scheduler, path='/')
    app.register_blueprint(api_blueprint, url_prefix='/scheduler_api/v1')

    return app
