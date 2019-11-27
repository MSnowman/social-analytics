"""
File used to schedule events such as data ingestion (Stock Price/Volume Data).

stock_price_job(s) are scheduled for 4:01 EST each weekday 1 minute after the NYSE closes.  Th Job runs on an AWS EC2
instance which runs on GMT time therefor the schedules below are set to 08:01 and not 16:01.

"""
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)

sys.path.insert(0, parentdir)

import schedule
import time
from schedulerapp.main.config import config_vars
import requests
import getopt


def get_batch_request_details(argv):
    try:
        opts, args = getopt.getopt(argv, "m:f:u:e:", ["market_analysis=", "frequency=", "user_id=", "env="])
    except getopt.GetoptError as err:
        print(err)
        print('tweepyStreamApp.py -m <market_analysis> -f <frequency> -u <user_id> -e <env>')
        sys.exit(2)
    market_analysis = None
    frequency = None
    user_id = None
    env = None
    for opt, arg in opts:
        if opt == '-h':
            print('tweepyStreamApp.py -m <market_analysis> -f <frequency> -u <user_id> -e <env>')
            sys.exit()
        elif opt in ("-m", "--market_analysis"):
            market_analysis = arg
        elif opt in ("-f", "--frequency"):
            frequency = arg
        elif opt in ("-u", "--user_id"):
            user_id = arg
        elif opt in ("-e", "--env"):
            env = arg

    payload = {'process': 'stock_quotes',
               'market_analysis': market_analysis,
               'env': env,
               'user_id': user_id}

    batch_url = config_vars.BATCH_URL
    batch_request_url = batch_url + 'start_stock_quote'
    return batch_request_url, payload, frequency


if __name__ == "__main__":
    batch_details = get_batch_request_details(sys.argv[1:])
    request_url = batch_details[0]
    request_payload = batch_details[1]


    def request_batch(url=request_url, payload=request_payload):
        requests.post(url, json=payload)

    schedule.every().monday.at("16:01").do(request_batch)
    schedule.every().tuesday.at("16:01").do(request_batch)
    schedule.every().wednesday.at("16:01").do(request_batch)
    schedule.every().thursday.at("16:01").do(request_batch)
    schedule.every().friday.at("16:01").do(request_batch)

    while True:
        schedule.run_pending()
        time.sleep(1)
