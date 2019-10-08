from subprocess import Popen
from sharedUtils.processManager import ProcessManager
import requests
import json
from streamingapp.main.config import config_by_name


def start_stream(data):
    queue = data['queue']
    user_id = data['user_id']
    topic = data['topic']
    network_configs = config_by_name[data['env']]
    ANALYSIS_URL = network_configs.ANALYSIS_URL
    terms_url = ANALYSIS_URL + 'get_market_analysis_search_terms/' + user_id + '/' + topic
    terms = requests.get(terms_url)
    terms_json = json.loads(terms.text)
    search_terms = '\"' + str(terms_json['search_terms']) + '\"'
    config_key = data['config_key']
    env = data['env']
    file_path = get_file_path()
    terms = ['python3', file_path, '-q', queue, '-s', search_terms, '-t', topic, '-u',
             user_id, '-c', config_key, '-e', env]
    Popen(terms)
    return 'Stream started', 201


def stop_stream(data):
    user_id = data['user_id']
    file_path = get_file_path(user_id)
    manager = ProcessManager(file_path)
    manager.kill()
    return 'Stream stopped', 201


def get_file_path():
    #file_path = '/home/ec2-user/twitter_data_analysis_api/streamingapp/main/streamer/tweepyStreamApp.py'
    file_path = '/Users/michaelsnow/PycharmProjects/GitHUB/social-analytics/streamingapp/main/streamer/' \
                'tweepyStreamApp.py'
    #test_path = '/Users/michaelsnow/PycharmProjects/GitHUB/social-analytics/streamingapp/main/streamer/streamertest.py'
    return file_path


def health_check():
    return

#if __name__ == '__main__':
# data = {
#     "user_id": "tweet_database",
#     "topic": "pjp_index",
#     "queue": "string",
#     "search_terms": 0,
#     "config_key": "string",
#     "stream_status": True}
#     data['user_id'] = 1234
#     data['queue'] = 'abcd'
#     data['search_terms'] = '[\'a\', \'b\', \'c\']'
#     data['config_key'] = 'dfgjh'
    #print(str(data))
    # start_stream(data)

