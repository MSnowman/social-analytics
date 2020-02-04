"""
Module is used to create a training data set in order to be able to train a NLP model.  Data is pulled from MongoDB
where it is stored

"""

import pymongo
from pymongo.errors import AutoReconnect, ServerSelectionTimeoutError
from mlapp.main import utilities as utils
import random
from mlapp.main.config import config_vars

client = pymongo.MongoClient(config_vars.MONGO_URI)


def define_mongo_db(user_id):
    """
    :param user_id: group or user requesting the sample data.
    :return: mongo client db object specific to group
    """
    db = client[user_id]
    return db


def restore_TrainingData(user, topic_name):
    db = define_mongo_db(user)
    try:
        topic = db['metadata'].find_one({'topic': topic_name})
        training_data = TrainingData(user, topic_name)
        for a in topic['annotators']:
            training_data.add_annotator(a)
        return training_data
    except:
        print('Topic ' + topic_name + ' does not exist for user: ' + user)


class TrainingData:
    """
    Use this class to create a training data set for a NLP Classification Model
    Configuration details will be saved in MongoDB
    """

    def __init__(self, user, topic_name):
        self.user = user
        self.topic_name = topic_name.lower()
        self.description = ''
        self.training_table_name = utils.training_table_name(topic_name)
        self.annotators = []
        self.data_source_config = {}
        self.training_data_store_config = {}
        self.creation_date = ''
        self.new_training_data = ''
        self.annotating_training_data = ''
        self.cnx = utils.my_sql_cnx(config_vars.MYSQL_USER, config_vars.MYSQL_PASSWORD, config_vars.MYSQL_HOST, user)
        self.mongo_db = define_mongo_db(user)

    def __str__(self):
        return "Class: Training Data"

    def add_annotator(self, annotator):
        self.annotators.append(annotator)

    def update_annotator_columns(self, annotators):
        for annotator in annotators:
            try:
                utils.add_column_var45_to_table(self.cnx, 'annotator_' + annotator, self.training_table_name)
            except:
                pass

    def generate_new_training_data(self, word_filter=None, records=1):
        """
        :param word_filter: optional field.  String to refine the random record search in.  Default value is None
        :param records: number of sample data records you wish to return.  Default value is 25
        :return: mongo cursor object of sample data

        """
        topic_collection = self.mongo_db[self.topic_name]

        try:
            if word_filter is None:
                collection = topic_collection
                sample_query = [{'$sample': {'size': records}}]
                sample_data = collection.aggregate(sample_query)
                self.new_training_data = sample_data
                return "Successfully added " + str(records) + " new record/s to the training data"

            else:
                filtered_data = topic_collection.find({'$text': {'$search': word_filter}})
                sample_data = random.sample(list(filtered_data), records)
                self.new_training_data = sample_data
                return "Successfully added " + str(records) + " new record/s to the training data with world filter '"\
                       + word_filter + "'"

        except AutoReconnect:
            return "AutoReconnect Exception, please try reducing number of records for given world filter or reduce " \
                   "word filter to 1 string"
            pass
        except ServerSelectionTimeoutError:
            return "Something went wrong.  Please try later"
            pass

    def insert_new_training_data_to_db(self):

        """
        :param data: mongo cursor object of data
        :return: saves information to db
        """
        utils.insert_tweet_training_data_to_mysql(self.cnx, self.topic_name, self.training_table_name,
                                                  self.new_training_data)

    def get_annotators(self):
        return self.annotators

    def get_all_training_data(self, number=''):
        """
        results json of all data
        :param number: number of records
        :return: json of all training data
        """
        data = utils.get_training_data(self.cnx, 'all', self.training_table_name, number)
        table_columns = utils.get_table_column_names(self.cnx, self.training_table_name)

        json_data = utils.create_training_table_json(data, table_columns)

        return json_data

    def get_unclassified_training_data(self, number=''):
        data = utils.get_training_data(self.cnx, 'unclassified', self.training_table_name, number)
        table_columns = utils.get_table_column_names(self.cnx, self.training_table_name)

        json_data = utils.create_training_table_json(data, table_columns)

        return json_data

    def get_classified_training_data(self, number=''):
        data = utils.get_training_data(self.cnx, 'classified', self.training_table_name, number)
        table_columns = utils.get_table_column_names(self.cnx, self.training_table_name)

        json_data = utils.create_training_table_json(data, table_columns)
        return json_data

    def annotate_training_data(self, data, annotator):
        """
        :param data: list of listed pairs of data.  takes in unique ID and TRUE/FALSE Value
        :param annotator: name of annotator
        :return:
        """
        utils.annotate_training_data(self.cnx, self.training_table_name, data, 'annotator_' + annotator, self.annotators)

        return

    def save_topic_details(self):

        collection_name = self.mongo_db['metadata']
        collection_name.create_index('topic', unique=True)

        collection_name.find_one_and_update({'topic': self.topic_name},
                                            {'$set': {'training_table_name': self.training_table_name}},
                                            upsert=True)
        collection_name.find_one_and_update({'topic': self.topic_name},
                                            {'$set': {'annotators': self.annotators}},
                                            upsert=True)

    def delete_training_table(self):
        utils.drop_sql_table(self.cnx, self.training_table_name)

    def remove_annotators(self, annotators):
        """

        :param annotators: list of annotators
        :return:
        """

        annotator_columns = ['annotator_' + annotator for annotator in annotators]
        utils.drop_sql_columns(self.cnx, self.training_table_name, annotator_columns)
        for annotator in annotators:
            self.annotators.remove(annotator)
