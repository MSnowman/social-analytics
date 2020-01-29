from mlapp.main.nlp import TrainingData as td
from mlapp.main.nlp import TextClassifier as tc
from mlapp.main import utilities as utils
from mlapp.main.config import config_vars
from flask import jsonify


def setup_training_data(data):
    user_id = data['user_id']
    topic_name = data['topic_name']
    new_training_data = td.TrainingData(user_id, topic_name)
    new_training_data.generate_new_training_data()
    new_training_data.insert_new_training_data_to_db()
    new_training_data.save_topic_details()
    return "Successfully created training data for " + topic_name


def get_more_training_data(data):
    user_id = data['user_id']
    topic_name = data['topic_name']
    existing_training_data = td.restore_TrainingData(user_id, topic_name)
    try:
        existing_training_data.generate_new_training_data(data['word_filter'], data['number_records'])
    except:
        existing_training_data.generate_new_training_data(records=data['number_records'])
        return "Successfully added " + str(data['number_records']) + " new records containing to the training data.  " \
            "There was an error with the word filer.  Please try less records or reduce word filter complexity."

    existing_training_data.insert_new_training_data_to_db()
    return "Successfully added " + str(data['number_records']) + " new records containing " + data['word_filter'] +\
           " to the training data"


def get_all_training_data(user_id, topic_name):
    result = td.restore_TrainingData(user_id, topic_name)
    result = result.get_all_training_data()
    return result


def get_unclassified_data(user_id, topic_name):
    result = td.restore_TrainingData(user_id, topic_name)
    result = result.get_unclassified_training_data()
    return result


def get_classified_data(user_id, topic_name):
    result = td.restore_TrainingData(user_id, topic_name)
    result = result.get_classified_training_data()
    return result


def get_list_training_data_topics(user_id):
    cnx_connection = utils.my_sql_cnx(config_vars.MYSQL_USER, config_vars.MYSQL_PASSWORD, config_vars.MYSQL_HOST
                                      , user_id)
    cursor = cnx_connection.cursor()
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    return result


def add_annotators(data):
    user_id = data['user_id']
    topic_name = data['topic_name']
    annotators = data['annotators']
    training_data = td.restore_TrainingData(user_id, topic_name)
    for annotator in annotators:
        training_data.add_annotator(annotator)
    training_data.update_annotator_columns(annotators)
    training_data.save_topic_details()
    return "Successfully added "


def annotate_training_data(data):
    user_id = data['user_id']
    topic_name = data['topic_name']
    records = data['records']
    annotator = data['annotator']
    training_data = td.restore_TrainingData(user_id, topic_name)
    training_data.annotate_training_data(records, annotator)
    return "Success"


def classify_data(data):
    user_id = data['user_id']
    topic_name = data['topic_name']
    record_id = data['record_id']
    record_text = data['text']
    text_classifier = tc.TextClassifier(user_id, topic_name)
    text_classifier.train_classier()
    return str(record_id) + ' is Relevant? ' + text_classifier.is_relevant(record_text)



