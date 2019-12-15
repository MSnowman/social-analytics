from flask import Flask
from uiapp.main.config import config_by_name


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    return app


