from flask import Flask, Blueprint
from flask_restplus import Api
from streamingapp.main.config import config_by_name
from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    flask_bcrypt.init_app(app)
    from streamingapp.main.router.streamer_routes import ns_streams
    api_blueprint = Blueprint('api', __name__)
    api = Api(api_blueprint,
              title='TWITTER STREAM MANAGEMENT API',
              version=1.0,
              description='A RESTful web service for starting and stopping Twitter streams')
    api.add_namespace(ns_streams, path='/')
    app.register_blueprint(api_blueprint, url_prefix='/streaming_api/v1')

    return app



# {
#   "user_id": "Snowman",
#   "analysis_name": "JPM Chase",
#   "analysis_description": "Everything that is relevant to JPM Chase",
#   "analysis_terms": {"JPM":["Chase","Today's Snapshot","Today'sSnapshot","JP","JPMorgan","JamieDimon","Dimon"]"}
# }