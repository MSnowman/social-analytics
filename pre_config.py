import os
import boto3
import json
import pymongo

DEBUG = True


try:
    if os.environ['HOSTNAME'] == 'ip-10-2-1-46':
        env = 'AWS'
        print('AWS')
        s3_client = boto3.client('s3')
        s3_bucket_name = 'secure-app-config'
        s3_data_bucket_name = 'sample-reference-data'
        config_key = 'twitterappconfig.json'
        sample_data_key = 'pjp_index_sample_data.csv'
        s3_config_object = s3_client.get_object(Bucket=s3_bucket_name, Key=config_key)
        config_file = s3_config_object['Body'].read().decode('utf-8')
        app_config = json.loads(config_file)
        s3_pjp_index_sample_data = s3_client_data.get_object(Bucket=s3_data_bucket_name, Key=sample_data_key)

        """
        Simple Queue Service
        """
        sqs_queue_url = app_config['sqs_queue_url']

        """
        MongoDB
        """
        mongodb_host = app_config['MONGODB_URL']
        tweet_db = 'tweet_database'
        analysis_collection = 'analyses'
        config_collection = 'config'


        def tweet_collection():
            t_collection = pymongo.MongoClient(mongodb_host)[tweet_db][config_collection] \
                .find_one({'name': 'streaming_config'})['analysis']
            return t_collection
        """
        MySQL
        """
        mysql_user = app_config['mysql_user']
        mysql_password = app_config['mysql_password']
        mysql_host = app_config['mysql_host']
        mysql_database = app_config['mysql_database']

        """
        TweetCredentials
        """
        config_key2 = 'twitterconfig.json'
        s3_config_object2 = s3_client.get_object(Bucket=s3_bucket_name, Key=config_key2)
        config_file2 = s3_config_object2['Body'].read().decode('utf-8')
        app_config2 = json.loads(config_file2)

        consumer_key = app_config2['CONSUMER_KEY']
        consumer_secret = app_config2['CONSUMER_SECRET']
        access_token = app_config2['ACCESS_TOKEN']
        access_secret = app_config2['ACCESS_SECRET']

        """
        Flask
        """
        host = '0.0.0.0'
        port = '80'

        root_url = 'http://ec2-54-200-112-204.us-west-2.compute.amazonaws.com'
        site_url = {'square_url': root_url + '/square/',
                    'stream': root_url + '/stream/',
                    'kill': root_url + '/kill/',
                    'graph_data': root_url + '/graph_data/',
                    'analysis_stats': root_url + '/analysis_stats/',
                    'word_cloud': root_url + '/word_cloud/',
                    'mysql_stats': root_url + '/mysql_stats/',
                    'sod_batch': root_url + '/sod_batch/',
                    'create_analysis': root_url + '/create_analysis/',
                    'delete_analysis': root_url + '/delete_analysis/'}

        flask_user = app_config['BASIC_AUTH_USERNAME']
        flask_credentials = app_config['BASIC_AUTH_PASSWORD']

        """
        Streamer
        """
        streamer_script = "/home/ec2-user/TwitterAPIProject"
        steamer_status = "Off"

        """
        Batch
        """
        sod_batch_script = "/home/ec2-user/TwitterAPIProject"

except KeyError:

    print('Local')
    env = 'Local'

    path = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/AnalysisDataPipelineServicesconfig.JSON"
    tweet_creds = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/Twitterkeys.JSON"
    with open(path, "r") as file:
        app_config = json.load(file)

    with open(tweet_creds, "r") as file2:
        tweet_config = json.loads(file2.read())

    """
    Simple Queue Service
    """
    sqs_queue_url = app_config['sqs_queue_url']

    """
    MongoDB
    """
    mongodb_host = app_config['mongodb_host']
    tweet_db = app_config['tweet_db']
    analysis_collection = app_config['analysis_collection']
    config_collection = 'config'
    aws_mongo_twitter_user = app_config['aws_mongo_twitter_user']
    aws_mongo_twitter_pwd = app_config['aws_mongo_twitter_pwd']


    def tweet_collection():
        t_collection = pymongo.MongoClient(mongodb_host)[tweet_db][config_collection] \
            .find_one({'name': 'streaming_config'})['analysis']
        return t_collection

    """
    MySQL
    """
    mysql_user = app_config['mysql_user']
    mysql_password = app_config['mysql_password']
    mysql_host = app_config['mysql_host']
    mysql_database = app_config['mysql_database']

    """
    Tweet
    """
    consumer_key = tweet_config['CONSUMER_KEY']
    consumer_secret = tweet_config['CONSUMER_SECRET']
    access_token = tweet_config['ACCESS_TOKEN']
    access_secret = tweet_config['ACCESS_SECRET']

    host = 'localhost'
    port = '5000'


    """
    Flask
    """
    root_url = 'http://localhost:5000'
    site_url = {'square_url': root_url+'/square/',
                'stream': root_url+'/stream/',
                'kill': root_url+'/kill/',
                'graph_data': root_url+'/graph_data/',
                'analysis_stats': root_url + '/analysis_stats/',
                'word_cloud': root_url + '/word_cloud/',
                'mysql_stats': root_url + '/mysql_stats/',
                'sod_batch': root_url + '/sod_batch/',
                'create_analysis': root_url + '/create_analysis/',
                'delete_analysis': root_url + '/delete_analysis/'}

    flask_user = app_config['BASIC_AUTH_USERNAME']
    flask_credentials = app_config['BASIC_AUTH_PASSWORD']

    """
    Streamer
    """
    streamer_script = app_config['streamer_script']
    steamer_status = "Off"

    """
    Batch
    """
    sod_batch_script = app_config['sod_batch_script']

    """
    Twilio
    """
    twilio_sid = app_config['twilio_sid']
    twilio_token = app_config['twilio_token']
    twilio_from = app_config['twilio_from']
    sms_to_numbers = app_config['sms_to_numbers']
