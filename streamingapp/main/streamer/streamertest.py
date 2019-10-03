#!/usr/bin/python

import sys
import getopt
import tweepy
from streamingapp.main.streamer.tweepyStreamClass import NewStreamListener
import boto3
import json
from ast import literal_eval
from flask import current_app as app
from streamingapp.main.service import streamer_services
import requests

data = {
  "user_id": "tweet_database",
  "topic": "pjp_index",
  "queue": "string",
  "search_terms": 0,
  "config_key": "string",
  "stream_status": True
}


# argv = streamer_services.start_stream(data)

tweet_creds = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/Twitterkeys.JSON"
ANALYSIS_URL = 'http://127.0.0.1:5002/'

terms_url = ANALYSIS_URL + 'get_market_analysis_search_terms/' + data['user_id'] + '/' + data['topic']
# terms_url = app.config['ANALYSIS_URL'] + 'get_market_analysis_search_terms/' + user_id + '/' + topic
terms = requests.get(terms_url)
terms_json = json.loads(terms.text)

data['search_terms'] = terms_json['search_terms']

with open(tweet_creds, "r") as file2:
    tweet_config = json.loads(file2.read())

#print(data['search_terms'])


def start(data):
    print(data['user_id'])
    print(data['topic'])

    auth = tweepy.OAuthHandler(consumer_key=tweet_config['CONSUMER_KEY'],
                               consumer_secret=tweet_config['CONSUMER_SECRET'])
    auth.set_access_token(tweet_config['ACCESS_TOKEN'],
                          tweet_config['ACCESS_SECRET'])
    api = tweepy.API(auth)
    stream_listener = NewStreamListener(queue_url=data['queue'], topic=data['topic'], user_id=data['user_id'])
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=data['search_terms'], languages=['en'])


# def get_creds(config_key):
#     """Function to get credentials from S3. Returns credentials."""
#     s3_client = boto3.client('s3')
#     s3_bucket_name = 'secure-app-config'
#     #config_key = 'twitterconfig.json'
#     s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=config_key)
#     file = s3_object['Body'].read().decode('utf-8')
#     twitter_config = json.loads(file)
#     return twitter_config


if __name__ == "__main__":
    start(data)