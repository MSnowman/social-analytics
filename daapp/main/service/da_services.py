from daapp.main.analysis import market_data_analysis as mda
import json
from bson import json_util


def create_market_data_analysis(data):
    db_name = data['user_id']
    analysis_name = data['analysis_name']
    description = data['analysis_description']
    terms = data['analysis_terms']

    analysis = mda.MarketDataAnalysis(db_name, analysis_name, description, terms)
    analysis.save_json_to_mongo()
    return 'Successfully created ' + analysis_name


def update_market_data_analysis(data):
    db_name = data['user_id']
    analysis_name = data['analysis_name']
    description = data['analysis_description']
    terms = data['analysis_terms']

    analysis = mda.restore_market_analysis(db_name, analysis_name)
    analysis.update_description(description)
    #analysis.add_streaming_terms()


def get_list_of_market_analyses(user_id):
    market_analyses = mda.get_list_of_analyses(user_id)
    return market_analyses


def get_market_analysis_details(user_id, analysis_name):
    market_analysis = mda.restore_market_analysis(user_id, analysis_name)
    market_analysis = market_analysis.create_json()
    return market_analysis


def get_market_analysis_search_terms(user_id, analysis_name):
    market_analysis = mda.restore_market_analysis(user_id, analysis_name)
    search_terms = market_analysis.get_streaming_terms_list()
    data = {'search_terms': search_terms}
    temp_file = json.dumps(data, indent=4)
    search_terms = json_util.loads(temp_file)
    return search_terms


def get_market_analysis_tickers(user_id, analysis_name):
    market_analysis = mda.restore_market_analysis(user_id, analysis_name)
    tickers = market_analysis.get_streaming_keys_list()
    data = {'tickers': tickers}
    temp_file = json.dumps(data, indent=4)
    tickers = json_util.loads(temp_file)
    return tickers
