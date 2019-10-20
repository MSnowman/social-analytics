from flask_restplus import Namespace, Resource, fields
from batchapp.main.service import batch_services

ns_batch = Namespace('batch', description='batch Start/Stop/Health Operations')

batch = ns_batch.model('Batch', {
    'process': fields.String(required=True, enum=['stock_quotes'], description='Process to batch'),
    'market_analysis': fields.String(required=False, description='Name of analysis for stock quote batch'),
    'env': fields.String(required=False, description="Environment variable omitted = prod"),
    'user_id': fields.String(required=False, decription="User ID Owning the Batch"),
})


@ns_batch.route('start_stock_quote')
class StartBatch(Resource):
    @ns_batch.doc('start_stock_quote')
    @ns_batch.expect(batch, validate=True)
    @ns_batch.response(409, 'Batch not started - already running.  Stop then start.')
    def post(self):
        """Start Stock Quote Batch"""
        return batch_services.get_stock_quotes(data=ns_batch.payload)


# @ns_batch.route('stop')
# class StopScheduler(Resource):
#     @ns_batch.doc('stop_batch')
#     @ns_batch.expect(batch, validate=True)
#     @ns_batch.response(409, 'Scheduler not running.  Nothing to stop')
#     def post(self):
#         """Stop Scheduler"""
#         return scheduler_services.stop_stock_quote_scheduler(data=ns_batch.payload)


