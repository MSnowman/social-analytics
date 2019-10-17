from batchapp.main.dataconnections import alpha_advantage as aa
import requests
import json
from batchapp.main.config import config_by_name
from batchapp.main.service import mysql_ingestion as msi


def get_stock_tickers(data):
    env = data['env']
    usr_id = data['user_id']
    market_analysis = data['market_analysis']
    network_configs = config_by_name[env]
    da_url = network_configs.ANALYSIS_URL
    ticker_url = da_url + 'get_market_analysis_tickers/' + usr_id + '/' + market_analysis
    results = requests.get(ticker_url)
    results_json = json.loads(results.text)
    tickers = results_json['tickers']
    return tickers


def get_stock_quotes(data):
    tickers = get_stock_tickers(data)
    env = data['env']
    network_configs = config_by_name[env]
    alpha_key = network_configs.ALPHA_ADVANTAGE_KEY

    for ticker in tickers:
        msi.pipe_prices_to_mysql(ticker, 'USD', alpha_key)

    return
