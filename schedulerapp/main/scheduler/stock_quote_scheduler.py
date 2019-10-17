"""
File used to schedule events such as data ingestion (Stock Price/Volume Data).

stock_price_job(s) are scheduled for 4:01 EST each weekday 1 minute after the NYSE closes.  Th Job runs on an AWS EC2
instance which runs on GMT time therefor the schedules below are set to 08:01 and not 16:01.

"""
import schedule
import time
#import Analysis.DataAnalysis as da#
#import dbConnections.StockPricesToMySQL as smsql
from schedulerapp.main import config_by_name
import requests
import json


def get_stock_quotes(data):
    configs = config_by_name[data['env']]
    payload = data
    batch_url = configs.BATCH_URL
    request_url = batch_url + 'start_stock_quote'
    requests.post(request_url, json=payload)



#stock_tickers = da.restore_analysis('pjp_index')
#stock_tickers = stock_tickers.get_streaming_keys_list()


# def stock_price_job(tickers=stock_tickers):
#     error_count = 0
#     for ticker in tickers:
#         if error_count < 5:
#             try:
#                 smsql.pipe_prices_to_mysql(ticker, 'USD')
#             except:
#                 error_count += 1
#                 print("There has been an error")
#                 smsql.pipe_prices_to_mysql(ticker, 'USD')
#
#
# schedule.every().monday.at("08:01").do(stock_price_job)
# schedule.every().tuesday.at("08:01").do(stock_price_job)
# schedule.every().wednesday.at("08:01").do(stock_price_job)
# schedule.every().thursday.at("08:01").do(stock_price_job)
# schedule.every().friday.at("08:01").do(stock_price_job)
#
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)



