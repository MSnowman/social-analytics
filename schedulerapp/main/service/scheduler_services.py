from schedulerapp.main.scheduler import stock_quote_scheduler as sqs


def start_schedule(data):
    if data['process_type'] == 'batch':
        if data['process'] == 'stock_quotes':
            start_stock_quote_batch_scheduler(data)
        else:
            return 'process not valid, please enter valid process of process_type'
    else:
        return 'process_type choice does not exist.  Please try again'


def start_stock_quote_batch_scheduler(data):
    sqs.get_stock_quotes(data)
    return


def stop_stock_quote_scheduler(data):
    return
