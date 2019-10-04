from subprocess import Popen
from sharedUtils.processManager import ProcessManager
import requests
import json

ANALYSIS_URL = 'http://127.0.0.1:5002/'


def start_stream(data):
    queue = data['queue']
    user_id = data['user_id']
    topic = data['topic']
    terms_url = ANALYSIS_URL + 'get_market_analysis_search_terms/' + user_id + '/' + topic
    terms = requests.get(terms_url)
    terms_json = json.loads(terms.text)
    search_terms = '\"' + str(terms_json['search_terms']) + '\"'
    config_key = data['config_key']
    env = data['env']
    file_path = get_file_path()
    terms = ['nohup', 'python3', file_path, '-q', queue, '-s', search_terms, '-t', topic, '-u',
             user_id, '-c', config_key, '-e', env, '&']
    print(terms)
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
    file_path ='/Users/michaelsnow/PycharmProjects/GitHUB/social-analytics/streamingapp/main/streamer/tweepyStreamApp.py'
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

