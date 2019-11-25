#!/usr/bin/python

import sys
import getopt
import tweepy
from streamingapp.main.streamer.tweepyStreamClass import NewStreamListener
import boto3
import json
from ast import literal_eval
import os


def start(argv):
    try:
        opts, args = getopt.getopt(argv, "q:s:t:u:c:e:a:", ["queue=", "search_terms=", "topic=", "user_id=", "config_key=",
                                                            "env=", "classify="])
    except getopt.GetoptError as err:
        print(err)
        print('tweepyStreamApp.py -q <queue_url> -s <search_terms> -t <topic> -u <user_id> -c <config_key> -e <env> '
              '-a <classify>')
        sys.exit(2)
    queue_url = None
    search_terms = None
    topic = None
    user_id = None
    config_key = None
    env = None
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
        elif opt in ("-c", "--config_key"):
            config_key = arg
        elif opt in ("-e", "--env"):
            env = arg
        elif opt in ("-a", "--classify"):
            classify = arg
    print(classify)
    search_terms = literal_eval(search_terms)
    search_terms = literal_eval(search_terms)

    creds = get_creds(os.getenv('BOILERPLATE_ENV') or 'loc')

    auth = tweepy.OAuthHandler(consumer_key=creds['CONSUMER_KEY'],
                               consumer_secret=creds['CONSUMER_SECRET'])

    auth.set_access_token(creds['ACCESS_TOKEN'],
                          creds['ACCESS_SECRET'])
    api = tweepy.API(auth)
    stream_listener = NewStreamListener(queue_url=queue_url, topic=topic, user_id=user_id, classify=classify)

    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=search_terms, languages=['en'])


def get_creds(environment):
    """Function to get credentials from local or S3. Returns credentials."""
    if environment == 'loc':
        tweet_creds = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/Twitterkeys.JSON"
        with open(tweet_creds, "r") as file2:
            twitter_config = json.loads(file2.read())
    else:
        s3_client = boto3.client('s3')
        s3_bucket_name = 'social-config'
        config_key = 'Social-configs.JSON'
        s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=config_key)
        file = s3_object['Body'].read().decode('utf-8')
        twitter_config = json.loads(file)

    return twitter_config


if __name__ == "__main__":
    start(sys.argv[3:])
