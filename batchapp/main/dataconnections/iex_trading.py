"""
Created on Sun Jul 7 2018

@author: Snowman

https://api.iextrading.com
All endpoints are prefixed with: https://api.iextrading.com/1.0

"""
import requests


def iex_base_url():
    base_url = "https://api.iextrading.com/1.0"
    return base_url


def ticker_string_test(ticker):
    try:
        assert type(ticker) == str
    except AssertionError:
        return print("Ticker needs to be a string")


def company_info(ticker):

    ticker_string_test(ticker)
    url = iex_base_url() + "/stock/" + ticker + "/company"
    page = requests.get(url)
    return page.json()


def earnings_info(ticker):

    ticker_string_test(ticker)
    url = iex_base_url() + "/stock/" + ticker + "/earnings"
    page = requests.get(url)
    return page.json()


def financial_info(ticker):

    ticker_string_test(ticker)
    url = iex_base_url() + "/stock/" + ticker + "/financials"
    page = requests.get(url)
    return page.json()


def key_stats(ticker):

    ticker_string_test(ticker)
    url = iex_base_url() + "/stock/" + ticker + "/stats"
    page = requests.get(url)
    return page.json()


def peers(ticker):

    ticker_string_test(ticker)
    url = iex_base_url() + "/stock/" + ticker + "/peers"
    page = requests.get(url)
    return page.json()


def similar_companies(ticker):

    ticker_string_test(ticker)
    url = iex_base_url() + "/stock/" + ticker + "/relevant"
    page = requests.get(url)
    return page.json()


def get_all_reference_data():

    url = iex_base_url() + "/ref-data/symbols"
    page = requests.get(url)
    return page.json()


def get_detailed_quotes(ticker):

    ticker_string_test(ticker)
    url = iex_base_url() + "/tops?symbol=" + ticker
    page = requests.get(url)
    return page.json()


