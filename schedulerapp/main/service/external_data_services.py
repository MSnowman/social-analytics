from schedulerapp.main.dataconnections import alpha_advantage as aa
import requests
import json
from schedulerapp.main.config import  config_by_name


def get_stock_tickers(data):
    env = data['env']
    usr_id = data['user_id']
    topic = data['topic']
    network_configs = config_by_name[env]
    da_url = network_configs.ANALYSIS_URL
    ticker_url = da_url + 'get_market_analysis_tickers/' + usr_id + '/' + topic
    results = requests.get(ticker_url)
    results_json = json.loads(results.text)
    tickers = results_json['tickers']
    return tickers


def get_stock_prices(data):
    tickers = get_stock_tickers(data)
    env = data['env']
    network_configs = config_by_name[env]
    alpha_key = network_configs.ALPHA_ADVANTAGE_KEY

    prices = []

    for ticker in tickers:
        price = aa.time_series_intraday(ticker, '1min', alpha_key)
        prices.append(price)

    return prices
