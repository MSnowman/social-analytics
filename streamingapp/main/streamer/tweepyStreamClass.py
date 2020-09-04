import tweepy
import boto3
from streamingapp.main.config import config_vars
import time
import json
import pymongo
import requests
from urllib3.exceptions import ProtocolError


class NewStreamListener(tweepy.StreamListener):

    def __init__(self, user_id, topic, queue_url, classify):
        super().__init__()
        self.db = user_id
        self.collection = topic
        self.queue_url = queue_url
        self.queue_client = boto3.client('sqs', region_name='us-west-2')
        self.classify = classify

    def on_connect(self):
        print("We're Connected!")
        print("Clasification Status = " + str(self.classify))

    def on_warning(self, notice):
        print(notice.text)
        print('warning')

    def on_status(self, status):
        print(status.text)
        print('status')

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            if self.classify is True:
                self.classify_data(json_data)

            else:
                pass
            # try:
            #     #response = self.queue_client.send_message(QueueUrl=self.queue_url,
            #     #                                         MessageBody=data)
            # except:
            #    pass
        except Exception as e:
            print(e)
            pass
        else:
            self.save_to_mongo_db(json_data)

    def classify_data(self, json_data):
        payload = {
            'user_id': self.db,
            'topic_name': self.collection,
            'data': json_data
        }
        ml_app_url = config_vars.ML_URL + 'streamer_classify'
        response = requests.post(ml_app_url, json=payload)
        print(response)
        return response.json()

    def save_to_mongo_db(self, data):
        try:
            db = pymongo.MongoClient(config_vars.MONGO_URI)
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
        with open('stream_errors.txt', 'a+') as file_object:
            if exception is ProtocolError:
                file_object.write(time.ctime() + " " + str(exception) + "\n")
            else:
                file_object.write(time.ctime() + " " + str(exception) + "\n")


