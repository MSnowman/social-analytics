from subprocess import Popen
from sharedUtils.processManager import ProcessManager
import requests
import json
from streamingapp.main.config import config_vars


def start_stream(data):
    queue = data['queue']
    user_id = data['user_id']
    topic = data['topic']
    terms_url = config_vars.ANALYSIS_URL + 'get_market_analysis_search_terms/' + user_id + '/' + topic
    terms = requests.get(terms_url)
    terms_json = json.loads(terms.text)
    search_terms = '\"' + str(terms_json['search_terms']) + '\"'
    config_key = data['config_key']
    env = data['env']
    classify = data['classify']
    file_path = config_vars.STREAMER_PATH
    terms = ['python3', file_path, '-q', queue, '-s', search_terms, '-t', topic, '-u',
             user_id, '-c', config_key, '-e', env, '-a', str(classify)]
    Popen(terms)
    return 'Stream started', 201


def stop_stream(data):
    user_id = data['user_id']
    file_path = config_vars.STREAMER_PATH()
    manager = ProcessManager(file_path)
    manager.kill()
    return 'Stream stopped', 201


def get_file_path():
    file_path = config_vars.STREAMER_PATH
    return file_path


def health_check():
    return



