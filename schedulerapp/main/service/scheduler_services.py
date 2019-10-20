from schedulerapp.main.scheduler import stock_quote_scheduler as sqs
from schedulerapp.main import config_by_name
from subprocess import Popen
from sharedUtils.processManager import ProcessManager


def start_schedule(data):
    if data['process_type'] == 'batch':
        if data['process'] == 'stock_quotes':
            start_stock_quote_batch_scheduler(data)
        else:
            return 'process not valid, please enter valid process of process_type'
    else:
        return 'process_type choice does not exist.  Please try again'


def start_stock_quote_batch_scheduler(data):
    market_analysis = data['market_analysis']
    frequency = data['frequency']
    env = data['env']
    user_id = data['user_id']
    file_path = get_file_path(data)
    terms = ['python3', file_path, '-m', market_analysis, '-f', frequency, '-u', user_id, '-e', env]
    Popen(terms)
    # sqs.get_stock_quotes(data)
    return 'Stream started', 201


def stop_stock_quote_scheduler(data):
    user_id = data['user_id']
    file_path = get_file_path(data)
    manager = ProcessManager(file_path)
    manager.kill()
    return 'Stream stopped', 201


def get_file_path(data):
    #file_path = '/home/ec2-user/twitter_data_analysis_api/streamingapp/main/streamer/tweepyStreamApp.py'
    network_config = config_by_name[data['env']]
    if data['process_type'] == 'batch':
        if data['process'] == 'stock_quotes':
            file_path = network_config.STOCK_QUOTE_SCHEDULER_PATH
        else:
            return 'path does not exist' + " " + data['process']
    else:
        return 'process does not exist'

    return file_path
