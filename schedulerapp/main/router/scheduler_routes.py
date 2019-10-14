from flask_restplus import Namespace, Resource, fields
from schedulerapp.main.service import scheduler_services

ns_scheduler = Namespace('scheduler', description='Schedule Start/Stop/Health Operations')

scheduler = ns_scheduler.model('Scheduler', {
    'process': fields.String(required=True, description='Process to schedule'),
    'market_analysis': fields.String(required=False, description='Name of analysis for stock quote scheduler'),
    'frequency': fields.String(required=False, description='Schedule frequency'),
    'env': fields.String(required=False, description="Environment variable omitted = prod"),
    'user_id': fields.String(required=False, decription="User ID Owning the Schedule"),
    'topic': fields.String(required=False, description="Topic with predefined terms to schedule for' ")
})


@ns_scheduler.route('start')
class StartSchedule(Resource):
    @ns_scheduler.doc('start_scheduler')
    @ns_scheduler.expect(scheduler, validate=True)
    @ns_scheduler.response(409, 'Scheduler not started - already running.  Stop then start.')
    def post(self):
        """Start Scheduler"""
        return scheduler_services.start_stock_quote_scheduler(data=ns_scheduler.payload)


@ns_scheduler.route('stop')
class StopScheduler(Resource):
    @ns_scheduler.doc('stop_scheduler')
    @ns_scheduler.expect(scheduler, validate=True)
    @ns_scheduler.response(409, 'Scheduler not running.  Nothing to stop')
    def post(self):
        """Stop Scheduler"""
        return scheduler_services.stop_stock_quote_scheduler(data=ns_scheduler.payload)


