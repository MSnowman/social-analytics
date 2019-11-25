import requests
import json
from batchapp.main.config import config_vars
from batchapp.main.service import mysql_ingestion as msi


def get_stock_tickers(data):
    usr_id = data['user_id']
    market_analysis = data['market_analysis']
    da_url = config_vars.ANALYSIS_URL
    ticker_url = da_url + 'get_market_analysis_tickers/' + usr_id + '/' + market_analysis
    results = requests.get(ticker_url)
    results_json = json.loads(results.text)
    tickers = results_json['tickers']
    return tickers


def get_stock_quotes(data):
    tickers = get_stock_tickers(data)
    usr_id = data['user_id']
    alpha_key = config_vars.ALPHA_ADVANTAGE_KEY

    for ticker in tickers:
        msi.pipe_prices_to_mysql(ticker, 'USD', alpha_key, usr_id)

    return
