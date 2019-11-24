"""
Creates a class to represent an analysis to pull data for.
Each instance to be used for a single analysis.
The self.name of the Class instance must be unique.

Example: You want to perform an analysis on the top 3 telecom stocks.
        You would create a class of Analysis
        Define the name
        Provide a description of the analysis
        Add all the key values you want to look for (e.g. Ticker)
            Add associated terms for that ticker (e.g. Company Name, Company products, etc.)

instance can be saved as JSON in mongoDB
    Requires MongoDb to be running

"""

import json
from bson import json_util
import pymongo
import time
from daapp.main.config import config_vars


client = pymongo.MongoClient(config_vars.MONGO_URI)


def market_analysis_collection(db_name):
    user_db = client[db_name]
    ma_collection = user_db["analyses"]
    ma_collection.create_index('name', unique=True)
    return ma_collection


def restore_market_analysis(db_name, name):
    """
    :param db_name: name of the database which is the user_id
    :param name: name of the analysis that is stored in the analyses collection
    :return: a class instance of MarketDataAnalysis
    """
    analysis = market_analysis_collection(db_name).find_one({'name': name})

    if analysis is None:
        return print('No analysis exists')
    else:
        return MarketDataAnalysis(db_name, analysis['name'], analysis['description'], analysis['terms'])


def get_list_of_analyses(db_name):
    analyses = []
    for analysis in market_analysis_collection(db_name).find():
        analyses.append(analysis['name'])
    return analyses


class MarketDataAnalysis:
    """
    This class is created to capture a streaming analysis.
    If defines the Name, Keys and associated Terms
    It also creates the Collection in Which the Tweets will be saved

    """
    def __init__(self, db_name, analysis_name, analysis_description, streaming_terms={}):
        self.streaming_terms = streaming_terms
        self.original_analysis_name = analysis_name.lower()
        self.analysis_name = analysis_name.lower()
        self.analysis_description = analysis_description
        self.db_name = db_name
        self.collection_name = analysis_name.lower()
        self.creation_date = ''
        self.version = 1
        self.history = []

    def __str__(self):
        return "Class:Analysis Name:" + self.get_analysis_name() + " Description:" +\
               self.get_analysis_description()

    def get_analysis_name(self):
        return self.analysis_name

    def get_original_analysis_name(self):
        return self.original_analysis_name

    def update_name(self, new_name):
        self.analysis_name = new_name.lower()

    def get_analysis_description(self):
        return self.analysis_description

    def update_description(self, new_description):
        self.analysis_description = new_description

    def get_streaming_terms_dict(self):
        return self.streaming_terms

    def get_history(self):
        return self.history

    def update_history(self):
        self.history.append({'version': self.version, 'name': self.get_analysis_name(),
                             'description': self.get_analysis_description(), 'term': self.get_streaming_terms_dict(),
                             'update_time': time.time()})

    def get_streaming_keys_list(self):
        keys = []
        for key in self.get_streaming_terms_dict():
            keys.append(key)
        return keys

    def get_streaming_terms_list(self):
        terms =[]
        for key in self.get_streaming_terms_dict():
            terms.append(key)
            if type(self.get_streaming_terms_dict()[key]) == list:
                for term in self.get_streaming_terms_dict()[key]:
                    terms.append(term)
            else:
                terms.append(self.get_streaming_terms_dict()[key])

        return sorted(terms)

    def get_streaming_terms_str(self):
        t_list = self.get_streaming_terms_list()
        r_list = ",".join(t_list).replace(",", ", ")
        return r_list

    def add_streaming_terms(self, key, terms):
        try:
            assert type(terms) == list
            self.streaming_terms.update({key: terms})
        except AssertionError:
            print("terms must be a list")

    def add_streaming_keys(self, keys):
        try:
            assert type(keys) == list
            for key in keys:
                self.streaming_terms.update({key:[]})
        except AssertionError:
            print('keys must be a list')

    def remove_streaming_key(self, key):
        self.streaming_terms.pop(key)

    def clear_streaming_key_terms(self, key):
        self.streaming_terms[key] = []

    def create_mongo_collection(self):
        collection_name = self.collection_name
        collection = client[self.db_name].create_collection(collection_name)
        return collection

    def create_json(self):
        data = {'name': self.get_analysis_name(), 'description': self.get_analysis_description(),
                'terms': self.get_streaming_terms_dict(), 'created_dated': time.time(), 'history': self.get_history()}
        temp_file = json.dumps(data, indent=4)
        insert_file = json_util.loads(temp_file)
        return insert_file

    def save_json_to_mongo(self):
        try:
            insert_file = self.create_json()
            market_analysis_collection(self.db_name).insert_one(insert_file)
            self.creation_date = time.time()
        except pymongo.errors.DuplicateKeyError:
            print("The Name of your Analysis already exists.  Please rename")

    def delete_analysis_from_mongo(self):
        try:
            market_analysis_collection(self.db_name).delete_one({"name": self.get_original_analysis_name()})
        except IndexError:
            print("Noting to delete")

    def update_analysis_in_mongo(self):
        self.update_history()
        insert_file = self.create_json()
        market_analysis_collection(self.db_name).replace_one({"name": self.get_original_analysis_name()}, insert_file)
        self.original_analysis_name = self.get_analysis_name()
        self.version += 1

