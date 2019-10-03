import tweepy
import boto3
from flask import app
import time
import json

print("hello")
#print(mongo.__dict__)
app


class NewStreamListener(tweepy.StreamListener):

    def __init__(self, user_id, topic, queue_url):
        super().__init__()
        #self.db = user_id
        self.topic = topic
        self.queue_url = queue_url
        self.queue_client = boto3.client('sqs', region_name='us-west-2')
        #self.db = mongo.cx(database=user_id, collection=topic)

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
            data = json.loads(data)
            # try:
            #     #response = self.queue_client.send_message(QueueUrl=self.queue_url,
            #     #                                         MessageBody=data)
            # except:
            #    pass
        except:
            pass
        else:
            print(data)
            self.save_to_mongo_db(data)

    def save_to_mongo_db(self, data):
        try:
            self.db.insert_one(data)

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
