#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:30:11 2018

@author: Snowman

Requires you to go to https://www.alphavantage.co and get an API Key

"""

import json
import requests


intervalTypes = ['1min', '5min', '15min', '30min', '60min']
sizes = ['full', 'compact']


def interval_type_test(interval):
    try:
        assert interval in intervalTypes
    except AssertionError:
        return print("Interval entered is not a valid interval.  Choose '1min','5min','15min','30min','60min'")


def size_test(size):
    try:
        assert size in sizes
    except AssertionError:
        return print("Defaulted to 'compact' size because sized entered is not a valid size. "
                     "Choose 'full' or 'compact' ")
    

def time_series_intraday(symbol, interval, api_key, size='compact'):
    """
    Get the intraday value of a stock or ETF.
    
    :symbol as string
    :interval: 1min, 5min, 15min, 30min, 60min
    size:
        compact = latest 100 calls
        full = all for the day
    :apiKey:
    
    """
    
    apiFunction = 'TIME_SERIES_INTRADAY'
    
    interval_type_test(interval)
    size_test(size)

    urlCreate = "https://www.alphavantage.co/query?function=" + apiFunction + "&symbol=" + symbol +\
                "&interval=" + interval + "&outputsize=" + size + "&apikey=" + api_key

    page = requests.get(urlCreate)
    json_data = json.loads(page.text)

    return json_data
    
    
def time_series_daily(symbol, api_key, size='compact'):
    """
    Get the value of a stock or ETF or past 100 days or max 20 years.
    Returns Open, High, Low, Close, Volume
    
    symbol as string
    size: 
        compact = last 100 days
        full = all up to 20 years
    
    """
    
    apiFunction = 'TIME_SERIES_DAILY'
    size_test(size)

    urlCreate = "https://www.alphavantage.co/query?function=" + apiFunction + "&symbol=" + symbol +\
                "&outputsize=" + size + "&apikey=" + api_key

    page = requests.get(urlCreate)
    json_data = json.loads(page.text)

    return json_data


def time_series_daily_adj(symbol, api_key, size='compact'):
    """
    Get the adjusted value of a stock or ETF or past 100 days or max 20 years.
    Returns Open, High, Low, Close, Volume, Daily Adj Close, Split/Dividend Events
    
    symbol as string
    size: 
        compact = last 100 days
        full = all up to 20 years
    
    """
    
    apiFunction = 'TIME_SERIES_DAILY_ADJUSTED'
    size_test(size)

    urlCreate = "https://www.alphavantage.co/query?function=" + apiFunction + "&symbol=" + symbol + \
                "&outputsize=" + size + "&apikey=" + api_key

    page = requests.get(urlCreate)
    json_data = json.loads(page.text)

    return json_data


def batch_stock_quotes(symbols, api_key):
    """
    Receive multiple stock quotes for different Symbols
    symbols is a list
    
    """
    
    apiFunction = 'BATCH_STOCK_QUOTES'

    urlCreate = "https://www.alphavantage.co/query?function=" + apiFunction + "&symbol=" + symbols + "&apikey=" + \
                api_key

    page = requests.get(urlCreate)
    json_data = json.loads(page.text)

    return json_data




