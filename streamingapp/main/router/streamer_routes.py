from flask_restplus import Namespace, Resource, fields
from streamingapp.main.service import streamer_services

ns_streams = Namespace('streams', description='Stream Start/Stop/Health Operations')

stream = ns_streams.model('Streams', {
    'user_id': fields.String(required=True, description='User ID Owning the Stream'),
    'topic': fields.String(required=False, description='Topic with predefined terms to search for'),
    'queue': fields.String(required=False, description='User Owned Queue to Write To'),
    'search_terms': fields.Integer(required=False, description='Set of Terms for Stream'),
    'config_key': fields.String(required=False, description='Name of config file in S3'),
    'env': fields.String(required=False, description="Environment variable omitted = prod"),
    'stream_status': fields.Boolean(readOnly=True, description='Is stream running or not')
})


@ns_streams.route('start')
class StreamStart(Resource):
    @ns_streams.doc('start_stream')
    @ns_streams.expect(stream, validate=True)
    @ns_streams.response(409, 'Stream not started - already running.  Stop then start.')
    def post(self):
        """Start Stream"""
        return streamer_services.start_stream(data=ns_streams.payload)


@ns_streams.route('stop')
class StreamStop(Resource):
    @ns_streams.doc('stop_stream')
    @ns_streams.expect(stream, validate=True)
    @ns_streams.response(409, 'Stream not stopped as it was not running.')
    def post(self):
        """Stop Stream"""
        return streamer_services.stop_stream(data=ns_streams.payload)


@ns_streams.route('healthcheck')
class HealthCheck(Resource):
    @ns_streams.doc('health_check')
    @ns_streams.marshal_with(stream, envelope='data')
    def get(self):
        """Returns Status of the Stream Requested"""
        return streamer_services.health_check()
