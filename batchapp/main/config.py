import os
import json

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class LocalConfig(Config):
    # For testing on on local machine
    ENV = 'local'
    try:
        path = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/AnalysisDataPipelineServicesconfig.JSON"
        tweet_creds = "/Users/michaelsnow/PycharmProjects/ApplicationKeys/Twitterkeys.JSON"
        with open(path, "r") as file:
            app_config = json.load(file)

        with open(tweet_creds, "r") as file2:
            tweet_config = json.loads(file2.read())

        MONGO_URI = app_config['mongodb_host']
        ANALYSIS_URL = app_config['ANALYSIS_URL']

        MYSQL_USER = app_config['mysql_user']
        MYSQL_PASSWORD = app_config['mysql_password']
        MYSQL_HOST = app_config['mysql_host']
        MYSQL_DATABASE = app_config['mysql_database']

        ALPHA_ADVANTAGE_KEY = app_config['alpha_advantage_key']

        create_stock_price_table_path = app_config['stock_price_table']

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
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    ANALYSIS_URL = 'Update url for da_app'
    MONGO_URI = 'Update URI for mongo instance'
    ML_URL = 'Enter ML_app url'



config_by_name = dict(
    loc=LocalConfig,
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
