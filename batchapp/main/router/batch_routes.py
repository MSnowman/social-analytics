from flask_restplus import Namespace, Resource, fields
from batchapp.main.service import batch_services

ns_batch = Namespace('batch', description='batch Start/Stop/Health Operations')

batch = ns_batch.model('Batch', {
    'process': fields.String(required=True, description='Process to batch'),
    'market_analysis': fields.String(required=False, description='Name of analysis for stock quote batch'),
    'env': fields.String(required=False, description="Environment variable omitted = prod"),
    'user_id': fields.String(required=False, decription="User ID Owning the Batch"),
    'topic': fields.String(required=False, description="Topic with predefined terms to batch for' ")
})


@ns_batch.route('start')
class StartBatch(Resource):
    @ns_batch.doc('start_batch')
    @ns_batch.expect(batch, validate=True)
    @ns_batch.response(409, 'Batch not started - already running.  Stop then start.')
    def post(self):
        """Start Batch"""
        return batch_services.get_stock_quotes(data=ns_batch.payload)


# @ns_batch.route('stop')
# class StopScheduler(Resource):
#     @ns_batch.doc('stop_batch')
#     @ns_batch.expect(batch, validate=True)
#     @ns_batch.response(409, 'Scheduler not running.  Nothing to stop')
#     def post(self):
#         """Stop Scheduler"""
#         return scheduler_services.stop_stock_quote_scheduler(data=ns_batch.payload)


