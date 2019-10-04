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


# data = {
#   "user_id": "tweet_db",
#   "topic": "pjp_index",
#   "queue": "string",
#   "search_terms": 0,
#   "config_key": "string",
#   "stream_status": True
# }
#
# argv = streamer_services.start_stream(data)

#tweet_creds = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/Twitterkeys.JSON"


#with open(tweet_creds, "r") as file2:
#   tweet_config = json.loads(file2.read())


def start(argv):
    try:
        opts, args = getopt.getopt(argv, "q:s:t:u:c:e:", ["queue=", "search_terms=", "topic=", "user_id=", "config=",
                                                          "env="])
    except getopt.GetoptError as err:
        print(err)
        print('tweepyStreamApp.py -q <queue_url> -s <search_terms> -t <topic> -u <user_id> -c <config> -e <env>')
        sys.exit(2)
    queue_url = None
    search_terms = None
    topic = None
    user_id = None
    config = None
    for opt, arg in opts:
        if opt == '-h':
            print('tweepyStreamApp.py -q <queue_url> -s <search_terms> -t <topic> -u <user_id> -c <config> -e <env>')
            sys.exit()
        elif opt in ("-q", "--queue"):
            queue_url = arg
        elif opt in ("-s", "--search_terms"):
            search_terms = arg
        elif opt in ("-t", "--topic"):
            topic = arg
        elif opt in ("-u", "--user_id"):
            user_id = arg
        elif opt in ("-c", "--config"):
            config = arg
        elif opt in ("-e", "--env"):
            env = arg

    print(" ")
    print(user_id)
    print(config)

    search_terms = literal_eval(search_terms)
    creds = get_creds(config)

    auth = tweepy.OAuthHandler(consumer_key=creds['CONSUMER_KEY'],
                               consumer_secret=creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'],
                          creds['ACCESS_SECRET'])
    api = tweepy.API(auth)
    stream_listener = NewStreamListener(queue_url=queue_url, topic=topic, user_id=user_id, env=env)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=search_terms, languages=['en'])


def get_creds(config_key):
    """Function to get credentials from local or S3. Returns credentials."""
    if config_key == 'loc':
        tweet_creds = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/Twitterkeys.JSON"
        with open(tweet_creds, "r") as file2:
            twitter_config = json.loads(file2.read())
    else:
        s3_client = boto3.client('s3')
        s3_bucket_name = 'secure-app-config'
        config_key = 'twitterconfig.json'
        s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=config_key)
        file = s3_object['Body'].read().decode('utf-8')
        twitter_config = json.loads(file)

    return twitter_config


if __name__ == "__main__":
    start(sys.argv[3:])
