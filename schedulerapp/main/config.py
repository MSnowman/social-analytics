import os
import json
import boto3
from botocore.exceptions import ClientError

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class LocalConfig(Config):
    # For testing on on local machine
    ENV = 'local'
    DEBUG = True
    try:
        path = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/AnalysisDataPipelineServicesconfig.JSON"
        tweet_creds = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/Twitterkeys.JSON"
        with open(path, "r") as file:
            app_config = json.load(file)

        with open(tweet_creds, "r") as file2:
            tweet_config = json.loads(file2.read())

        MONGO_URI = app_config['mongodb_host']
        ANALYSIS_URL = app_config['ANALYSIS_URL']
        BATCH_URL = app_config['BATCH_URL']
        ML_URL = app_config['ML_URL']

        ALPHA_ADVANTAGE_KEY = app_config['alpha_advantage_key']
        STOCK_QUOTE_SCHEDULER_PATH = app_config['stock_quote_scheduler_path']

    except FileNotFoundError as e:
        print('Local App Config file not found')


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root1234@127.0.0.1:3306/Herd_Application_Data'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """AWS S3 Configurations    """
    ENV = 'production'
    DEBUG = False
    try:
        s3 = boto3.client('s3')
        s3_bucket_name = 'social-config'
        config_key = 'Social-configs.JSON'
        s3_config_object = s3.get_object(Bucket=s3_bucket_name, Key=config_key)
        config_file = s3_config_object['Body'].read().decode('utf-8')
        app_config = json.loads(config_file)

        MONGO_URI = app_config['mongodb_host']
        ANALYSIS_URL = app_config['ANALYSIS_URL']
        BATCH_URL = app_config['BATCH_URL']
        ML_URL = app_config['ML_URL']

        ALPHA_ADVANTAGE_KEY = app_config['alpha_advantage_key']
        STOCK_QUOTE_SCHEDULER_PATH = app_config['STOCK_QUOTE_SCHEDULER_PATH']

    except ClientError as e:
        print(e, "Client Error on AWS connecting to S3. Expected if running local.")
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    loc=LocalConfig,
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

config_vars = config_by_name[os.getenv('BOILERPLATE_ENV') or 'loc']
