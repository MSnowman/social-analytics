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
        config_path = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/AnalysisDataPipelineServicesconfig.JSON"
        with open(config_path, "r") as file:
            app_config = json.load(file)

        MONGO_URI = app_config['mongodb_host']

        MYSQL_USER = app_config['mysql_user']
        MYSQL_PASSWORD = app_config['mysql_password']
        MYSQL_HOST = app_config['mysql_host']

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
    try:
        s3 = boto3.client('s3')
        s3_bucket_name = 'social-config'
        config_key = 'Social-configs.JSON'
        s3_config_object = s3.get_object(Bucket=s3_bucket_name, Key=config_key)
        config_file = s3_config_object['Body'].read().decode('utf-8')
        app_config = json.loads(config_file)

        MONGO_URI = app_config['mongodb_host']
        
        MYSQL_USER = app_config['mysql_user']
        MYSQL_PASSWORD = app_config['mysql_password']
        MYSQL_HOST = app_config['mysql_host']

    except ClientError as e:
        print(e, "Client Error on AWS connecting to S3. Expected if running local.")

    DEBUG = False


config_by_name = dict(
    loc=LocalConfig,
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

config_vars = config_by_name[os.getenv('BOILERPLATE_ENV') or 'loc']
