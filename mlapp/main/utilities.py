import mysql.connector
import json
from pandas import datetime as dt


def yes_no_test(answer):
    yes_no = ['yes', 'no']
    try:
        assert answer in yes_no
    except AssertionError:
        return print("Defaulted to 'yes' because sized entered is not a valid size. "
                     "Choose 'full' or 'compact' ")


def get_listed_data(input_list, key):
    data_list = []
    for i in input_list:
        data_list.append(i[key])
    if not data_list:
        return 'NULL'
    else:
        return str(data_list).strip('[]')


def my_sql_cnx(user, password, host, database):

    try:
        cnx = mysql.connector.connect(user=user, password=password,
                                      host=host, database=database)
    except mysql.connector.ProgrammingError:
        cnx = mysql.connector.connect(user=user, password=password,
                                      host=host)
        mycursor = cnx.cursor()
        mycursor.execute("CREATE DATABASE " + database)
        cnx = mysql.connector.connect(user=user, password=password,
                                      host=host, database=database)
        pass

    return cnx


def training_table_name(topic):
    table_name = str.lower(topic)
    table_name = table_name + "_training_data"
    return table_name


def create_tweet_training_data_sql_table(cnx, table_name):
    """

    :param cnx: MySQL database connection
    :param table_name: name of table to create within the database
    :return: creation status
    """

    sql = 'CREATE TABLE ' + table_name + '(' \
        'unique_tweet_id varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, '\
        'tweet_time datetime NULL,'\
        'topic_name varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,'\
        'tweeter varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,' \
        'tweeter_screen_name varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,' \
        'tweet_text varchar(280) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,' \
        'tweet_hashtags varchar(280) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,' \
        'ticker varchar(280) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,' \
        'relevant varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,' \
        'PRIMARY KEY (`unique_tweet_id`)'\
        ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'

    my_cursor = cnx.cursor()
    my_cursor.execute(sql)


def insert_tweet_training_data_to_mysql(cnx, topic, table_name, data):
    """
    :param cnx: MySQL database connection
    :param topic: name of the topic
    :param table_name: name of table to create within the database
    :param data: MongoDB cursor object
    :return: save status

    """

    count = 0
    integrity_errors = 0
    database_errors = 0
    value_errors = 0
    key_errors = 0

    my_cursor = cnx.cursor()
    my_cursor.execute("SHOW TABLES")
    results = my_cursor.fetchall()
    table_name_check = (table_name,)

    if table_name_check not in results:
        create_tweet_training_data_sql_table(cnx, table_name)
        print("A new table was created with name: ", table_name)
    print("importing....")
    for tweet in data:
        count += 1

        try:
            tu = tweet['user']
            ts = format_str_tweet_time(tweet['created_at'])
            val = (tweet['id_str'],
                   ts,
                   topic,
                   tu['id_str'],
                   tu['screen_name'],
                   tweet['text'],
                   get_listed_data(tweet['entities']['hashtags'], 'text'))

            sql = 'INSERT INTO ' + table_name + ' (' \
                  'unique_tweet_id, ' \
                  'tweet_time, ' \
                  'topic_name, ' \
                  'tweeter, ' \
                  'tweeter_screen_name, ' \
                  'tweet_text, ' \
                  'tweet_hashtags)' \
                  'VALUES (%s, %s, %s, %s, %s, %s, %s)'
            my_cursor.execute(sql, val)
            cnx.commit()
        except mysql.connector.errors.IntegrityError:
            integrity_errors += 1
            pass

        except mysql.connector.errors.DatabaseError:
            database_errors += 1
            pass

        except ValueError:
            value_errors += 1
            pass

        except KeyError:
            key_errors += 1
            pass

    print('Total row insert attempts: ' + str(count))
    print('Total mysql.IntegrityErrors: ' + str(integrity_errors))
    print('Total mysql.DatabaseErrors: ' + str(database_errors))
    print('Total ValueErrors: ' + str(value_errors))
    print('Total KeyErrors: '+str(key_errors))
    print('Total rows inserted: ' + str(count-integrity_errors-database_errors-value_errors))

    return


def add_column_var45_to_table(cnx, column_name, table_name):
    """
    add a VARCHAR(45) column to a sql table
    :param cnx: MySQL database connection
    :param column_name: name of column
    :param table_name: Name of the table you want to add the column to
    :return: add status
    """

    my_cursor = cnx.cursor()

    sql = 'ALTER TABLE ' + table_name + \
        ' ADD ' + column_name + ' VARCHAR(45);'

    my_cursor.execute(sql)
    cnx.commit()
    return


def get_training_data(cnx, data_type, table_name, annotator='', number=''):
    """
    get data from a table in MySQL in JSON
    :param cnx: MySQL database connect
    :param data_type: ['all', 'classified', 'unclassified']
    :param table_name: name of table to get data from
    :param annotator: not used.  May be used to pass an annotator name to just see data not classified by an annotator.
    :param number of records to return.  Optional and not sure this will be used
    :return: object of data from table
    """

    if data_type.lower() == 'all' and annotator == '':
        sql = 'SELECT * FROM ' + cnx.database + '.' + table_name + ';'

    elif data_type.lower() == 'unclassified' and annotator == '':
        sql = 'SELECT * FROM ' + cnx.database + '.' + table_name + ' WHERE relevant IS NULL;'

    elif data_type.lower() == 'classified' and annotator == '':
        sql = 'SELECT * FROM ' + cnx.database + '.' + table_name + ' WHERE relevant IS NOT NULL;'

    my_cursor = cnx.cursor()

    my_cursor.execute(sql)
    my_results = my_cursor.fetchall()

    return my_results


def annotate_training_data(cnx, table_name, data, annotator, annotators):
    """
    Update row values for annotator/s.  Will fetch data within the database update the values then calculate "relevant"
    coplumns based on the values of each annotator for that given ID.
    relevant = TRUE if at least one annotator deaming the record relevant and no annotator deaming the record not relevant
    :param cnx: MySQL database connect

    :param table_name: name of training data table
    :param data: List with embedded list of data [id:TRUE/FALSE]
    :param annotator: name of annotator
    :param annotators: list of annotators
    :return:
    """
    classified_data = create_training_table_json(get_training_data(cnx, 'classified', table_name),
                                                 get_table_column_names(cnx, table_name))

    annotator_columns = ['annotator_' + name for name in annotators]
    annotator_columns.remove(annotator)

    for row in data:
        if any(d['unique_tweet_id'] == row['record_id'] for d in classified_data['training_data']):

            tweet = get_item_from_json(classified_data, row['record_id'])
            annotator_results = [tweet[name] for name in annotator_columns]
            annotator_results.append(row['relevant'])

            if 'TRUE' in annotator_results and 'FALSE' in annotator_results:
                tweet['relevant'] = 'disagreement'
            elif 'TRUE' in annotator_results:
                tweet['relevant'] = 'TRUE'
            else:
                tweet['relevant'] = 'FALSE'

            sql = 'UPDATE ' + cnx.database + '.' + table_name + ' SET relevant = %s, ' + annotator + ' = %s, ' + \
                  'ticker = %s WHERE unique_tweet_id = %s'
            val = (tweet['relevant'], row['relevant'], str(row['tickers']).strip('[]'), row['record_id'])
            my_cursor = cnx.cursor()
            my_cursor.execute(sql, val)
            cnx.commit()

        else:
            sql = 'UPDATE ' + cnx.database + '.' + table_name + ' SET relevant = %s, ' + annotator + ' = %s, ' + \
                'ticker = %s WHERE unique_tweet_id = %s'
            val = (row['relevant'], row['relevant'], str(row['tickers']).strip('[]'), row['record_id'])
            print(val)
            my_cursor = cnx.cursor()
            my_cursor.execute(sql, val)
            cnx.commit()

    return


def update_row_relevancy_in_sql(cnx, table_name, annotators):
    """
    :param cnx: MySQL database connect
    :param table_name: name of training data table
    :param annotators: unique record id in table
    :return:
    """


def drop_sql_table(cnx, table_name):

    my_cursor = cnx.cursor()
    sql = "DROP TABLE " + table_name
    my_cursor.execute(sql)


def drop_sql_columns(cnx, table_name, columns):

    my_cursor = cnx.cursor()

    for column in columns:
        sql = "ALTER TABLE " + table_name + " DROP COLUMN " + column + ";"
        my_cursor.execute(sql)


def get_table_column_names(cnx, table_name):

    my_cursor = cnx.cursor()
    sql = "SHOW columns FROM " + table_name
    my_cursor.execute(sql)
    results = my_cursor.fetchall()

    column_names = []

    for result in results:
        column_names.append(result[0])

    return column_names


def format_str_tweet_time(tweet_time):
    tsr = dt.strptime(tweet_time, '%a %b %d %H:%M:%S +0000 %Y')
    return str(tsr)


def format_datetime_tweet_time(tweet_time):
    tsr = dt.strftime(tweet_time, '%a %b %d %Y %H:%M:%S +0000')
    return str(tsr)


def create_training_table_json(training_data, table_columns):

    data = {'training_data': [],
            'training_stats': {'relevant': '', 'not_relevant': '', 'unclassified': ''}}

    relevant = 0
    not_relevant = 0
    unclassified = 0
    for row in training_data:
        record = {}
        for column in table_columns:
            record[column] = ''
        for column in range(len(table_columns)):
            record[table_columns[column]] = row[column]
        record['tweet_time'] = format_datetime_tweet_time(record['tweet_time'])
        data['training_data'].append(record)
        if row[7] == "TRUE":
            relevant += 1
        elif row[7] == "FALSE":
            not_relevant += 1
        else:
            unclassified += 1
    data['training_stats']['relevant'] = relevant
    data['training_stats']['not_relevant'] = not_relevant
    data['training_stats']['unclassified'] = unclassified

    data = json.dumps(data, indent=4)
    json_file = json.loads(data)
    return json_file


def get_item_from_json(json_object, tweet_id):

    return [obj for obj in json_object['training_data'] if obj['unique_tweet_id'] == tweet_id][0]


