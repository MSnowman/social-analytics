import tweepy
import boto3
from streamingapp.main.config import config_by_name
import time
import json
import pymongo
import requests


class NewStreamListener(tweepy.StreamListener):

    def __init__(self, user_id, topic, queue_url, env):
        super().__init__()
        self.db = user_id
        self.collection = topic
        self.queue_url = queue_url
        self.queue_client = boto3.client('sqs', region_name='us-west-2')
        self.env_config = config_by_name[env]

    def mongo_connection(self):
        mongo_uri = self.env_config.MONGO_URI
        client = pymongo.MongoClient(mongo_uri)
        return client

    def on_connect(self):
        print("We're Connected!")

    def on_warning(self, notice):
        print(notice.text)
        print('warning')

    def on_status(self, status):
        print(status.text)
        print('status')

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            classification = self.classify_data(json_data)
            print(classification)
            print("New Data")
            # try:
            #     #response = self.queue_client.send_message(QueueUrl=self.queue_url,
            #     #                                         MessageBody=data)
            # except:
            #    pass
        except:
            pass
        else:
            #print(data)
            self.save_to_mongo_db(json_data)

    def classify_data(self, json_data):
        payload = {
            'user_id': self.db,
            'topic_name': self.collection,
            'record_id': json_data['id'],
            'text': json_data['text']
        }
        ml_app_url = self.env_config.ML_URL + 'mlapi/v1/classify_data'
        response = requests.post(ml_app_url, json=payload)
        return response, response.json()

    def save_to_mongo_db(self, data):
        try:
            db = self.mongo_connection()
            db[self.db][self.collection].insert_one(data)

        except Exception as e:
            with open('mongo_errors.txt', 'a') as file_object:
                file_object.write(time.ctime() + " " + str(e) + " " + str(data) + " " + "\n")
        else:
            pass

    def on_error(self, status_code):
        if status_code == 420:
            return "ERROR!"
        else:
            return False

    def on_exception(self, exception):
        with open('stream_errors.txt', 'a') as file_object:
            file_object.write(str(exception) + "\n")

