from schedulerapp.main.scheduler import stock_quote_scheduler as sqs
from schedulerapp.main.service import external_data_services as eds


def start_stock_quote_scheduler(data):
    prices = eds.get_stock_prices(data)

    return prices


def stop_stock_quote_scheduler(data):
    return
