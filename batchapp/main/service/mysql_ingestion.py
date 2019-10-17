"""

Module pipes ingested stock market data into a MySQL database table

@Snowman 8/22/2018

"""

from batchapp.main.dataconnections import alpha_advantage as aa
import mysql.connector
import time
import pre_config

# Create MySQL connection
cnx = mysql.connector.connect(user=pre_config.mysql_user, password=pre_config.mysql_password,
                              host=pre_config.mysql_host,
                              database=pre_config.mysql_database)
mycursor = cnx.cursor()


intraday_intervals = aa.intervalTypes


def pipe_prices_to_mysql(ticker, ccy, alpha_key, interval='1min'):

    try:
        prices = aa.time_series_intraday(ticker, interval, alpha_key, 'full')
        price_keys = prices['Time Series (' + interval + ')'].keys()

    except KeyError:
        print(ticker + ' key error.  sleeping for 60 seconds')
        print(prices)
        time.sleep(60)
        pipe_prices_to_mysql(ticker, ccy, alpha_key, interval='1min')
        return

    except ConnectionError:
        print(ticker + ' connection error.  sleeping for 1 seconds')
        time.sleep(1)
        pipe_prices_to_mysql(ticker, ccy, alpha_key, interval='1min')
        return

    print("importing " + ticker + "....")
    count = 0
    for key in price_keys:
        count += 1
        interval_detail = prices['Time Series ('+interval+')'][key]
        try:
            val =(interval_detail['1. open'],
                  interval_detail['2. high'],
                  interval_detail['3. low'],
                  interval_detail['4. close'],
                  interval_detail['5. volume'],
                  ticker,
                  ccy,
                  key)

            sql = 'INSERT INTO stock_prices (' \
                    'open, ' \
                    'high, ' \
                    'low, ' \
                    'close, ' \
                    'volume, ' \
                    'ticker, ' \
                    'ccy, ' \
                    'time) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(sql, val)
            cnx.commit()
        except ValueError:
            pass

        except mysql.connector.IntegrityError:
            pass

    return print(count)


def pipe_1m_prices_to_mysql(ticker, ccy, alpha_key):
    pipe_prices_to_mysql(ticker, ccy, alpha_key, '1min')
    print('1 minute prices imported into SQL')


def pipe_5m_prices_to_mysql(ticker, ccy, alpha_key):
    pipe_prices_to_mysql(ticker, ccy, alpha_key, '5min')
    print('5 minute prices imported into SQL')


def pipe_15m_prices_to_mysql(ticker, ccy, alpha_key):
    pipe_prices_to_mysql(ticker, ccy, alpha_key, '15min')
    print('15 minute prices imported into SQL')


def pipe_30m_prices_to_mysql(ticker, ccy, alpha_key):
    pipe_prices_to_mysql(ticker, ccy, alpha_key, '30min')
    print('30 minute prices imported into SQL')


def pipe_60m_prices_to_mysql(ticker, ccy, alpha_key):
    pipe_prices_to_mysql(ticker, ccy, alpha_key, '60min')
    print('60 minute prices imported into SQL')
