from flask_restplus import Namespace, Resource, fields
from daapp.main.service import da_services

ns_da = Namespace('data analysis', description='Access the different types of data analyses')

listed_security = ns_da.model('ListedSecurity', {

}, description='{Ticker:[term1,term2]}')


market_data_analysis = ns_da.model('MarketDataAnalysis', {
    'user_id': fields.String(required=True, description='User Id creating the market data analysis.  Could be either an'
                                                        'individual or business account.'),
    'analysis_name': fields.String(required=True, description='Name of the analysis'),
    'analysis_description': fields.String(required=True, description='Description of the analysis'),
    'analysis_terms': fields.Nested(required=True, model=listed_security, description='Dictionary of {Ticker:'
                                                                                      '[description/terms]}')
})


@ns_da.route('create_market_analysis')
class SetupMarketAnalysis(Resource):
    @ns_da.doc('create_market_analysis')
    @ns_da.expect(market_data_analysis, validate=True)
    def post(self):
        """Setup market data analysis"""
        return da_services.create_market_data_analysis(data=ns_da.payload)


@ns_da.route('update_market_analysis')
class UpdateMarketAnalysis(Resource):
    @ns_da.doc('update_market_analysis')
    def put(self):
        """Update the details in an analysis"""
        return da_services.update_market_data_analysis(data=ns_da.payload)


@ns_da.route('get_list_of_market_analyses/<string:user_id>')
class GetListOfMarketAnalyses(Resource):
    @ns_da.doc('get_list_of_market_analysis')
    def get(self, user_id):
        """Get list of market analyses"""
        return da_services.get_list_of_market_analyses(user_id)


@ns_da.route('get_market_analysis_details/<string:user_id>/<string:analysis_name>')
class GetMarketAnalysisDetails(Resource):
    @ns_da.doc('get_market_analysis_details')
    def get(self, user_id, analysis_name):
        """Get the details of a given market analysis"""
        return da_services.get_market_analysis_details(user_id, analysis_name)


@ns_da.route('get_market_analysis_search_terms/<string:user_id>/<string:analysis_name>')
class GetMarketAnalysisStreamingTerms(Resource):
    @ns_da.doc('get_market_analysis_streaming_terms')
    def get(self, user_id, analysis_name):
        """Get the terms a streamer will listen for"""
        return da_services.get_market_analysis_search_terms(user_id, analysis_name)


@ns_da.route('get_market_analysis_tickers/<string:user_id>/<string:analysis_name>')
class GetMarketAnalysisTickers(Resource):
    @ns_da.doc('get_market_analysis_tickers')
    def get(self, user_id, analysis_name):
        """Get a list of tickers associated with the market analysis"""
        return da_services.get_market_analysis_tickers(user_id, analysis_name)





