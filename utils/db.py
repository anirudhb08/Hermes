#!/usr/bin/python
import sys, os
import psycopg2
import pandas as pd
from configparser import ConfigParser
from sqlalchemy import create_engine, text
from datetime import datetime, timezone, timedelta
 
def config(filename='db.ini', section='postgresql'):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filepath = os.path.join(__location__, filename)

    parser = ConfigParser()
    parser.read(filepath)
 
    # get section, default to postgresql
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filepath))
 
    return db_config

def connect():
    conn = None
    try:
        # read connection parameters and connect
        params = config()
        conn = psycopg2.connect(**params)

    except Exception as e:
        print('Could not connect to DB. Error: ' + str(e))

    return conn

def create_tickerdata():
    conn = connect()
    return create_tickerdata(conn) if conn is not None else False

def create_tickerdata(conn):
    # SCHEMA: (time, ticker, open, close, high, low, metric, value)
    create_query = \
    '''
    CREATE TABLE IF NOT EXISTS tickerdata(
    time BIGINT NOT NULL,
    ticker TEXT NOT NULL,
    open DOUBLE PRECISION NULL,
    close DOUBLE PRECISION NULL,
    high DOUBLE PRECISION NULL,
    low DOUBLE PRECISION NULL,
    metric TEXT NOT NULL,
    value DOUBLE PRECISION NULL,
    PRIMARY KEY (ticker, metric, time));
    '''

    index1_query = 'CREATE INDEX IF NOT EXISTS tickerdata_tmt ON tickerdata (ticker, metric, time DESC);'
    index2_query = 'CREATE INDEX IF NOT EXISTS tickerdata_tt ON tickerdata (ticker, time DESC);'

    try:
        with conn.cursor() as cur:
            cur.execute(create_query)
            cur.execute(index1_query)
            cur.execute(index2_query)
            conn.commit()
            return True

    except Exception as e:
        print(e)
        return False

def create_activitylog():
    conn = connect()
    return create_activitylog if conn is not None else False

def create_activitylog(conn):
    # SCHEMA: (time, ticker, activity, price, remarks)
    create_query = \
    '''
    CREATE TABLE IF NOT EXISTS activitylog(
    time BIGINT NOT NULL,
    ticker TEXT NOT NULL,
    activity TEXT NOT NULL,
    price DOUBLE PRECISION NULL,
    remarks TEXT NULL);
    '''

    index_query = 'CREATE INDEX IF NOT EXISTS activitylog_tt ON activitylog (ticker, time DESC);'

    try:
        with conn.cursor() as cur:
            cur.execute(create_query)
            cur.execute(index_query)
            conn.commit()
            return True

    except Exception as e:
        print(e)
        return False

def write_to_db(tablename, pd_frame):
    db_config = config()

    # Format: 'dialect+driver://username:password@host:port/database'
    engine_str = 'postgresql+psycopg2://' + db_config['user'] + ':' + db_config['password'] + '@' + db_config['host'] + '/' + db_config['database']
    engine = create_engine(engine_str)

    # Note: this can be optimized using this -- https://gist.github.com/ellisvalentiner/63b083180afe54f17f16843dd51f4394
    pd_frame.to_sql(tablename, engine_str, if_exists='append', index=False)

def get_engine():
    db_config = config()
    engine_str = 'postgresql+psycopg2://' + db_config['user'] + ':' + db_config['password'] + '@' + db_config['host'] + '/' + db_config['database']
    engine = create_engine(engine_str)
    return engine

def read_from_tickerdata(ticker, metric, tbegin, tend, tstep):
    # Both `tbegin` and `tend` should be in UNIX seconds
    engine = get_engine()

    select_query = \
    '''
    SELECT * FROM tickerdata
    WHERE ticker = '{0}' AND metric = '{1}' AND time >= {2} AND time <= {3} AND (time - {2}) % {4} = 0
    '''.format(ticker, metric, tbegin, tend, tstep)

    df = pd.read_sql_query(text(select_query), engine)
    return df

def read_from_activitylog(ticker, activity):
    engine = get_engine()

    select_query = \
    '''
    SELECT * FROM activitylog
    WHERE ticker = '{0}' AND activity = '{1}'
    '''.format(ticker, activity)

    df = pd.read_sql_query(text(select_query), engine)
    return df

def read_from_db(query):
    engine = get_engine()

    return pd.read_sql_query(query, engine)

def setup():
    conn = connect()
    if conn is not None:
        create_tickerdata(conn)
        create_activitylog(conn)

def test_setup():
    date_today = datetime(2018, 1, 1, tzinfo=timezone.utc).timestamp()
    date_tomorrow = datetime(2018, 1, 2, tzinfo=timezone.utc).timestamp()

    try:
        read_from_db("DELETE FROM tickerdata WHERE ticker = 'test_setup' RETURNING *")
    except Exception as e:
        pass
    try:
        read_from_db("DELETE FROM activitylog WHERE ticker = 'test_setup' RETURNING *")
    except Exception as e:
        pass

    ticker_df = pd.DataFrame({
        'time': [date_today, date_tomorrow],
        'ticker': ['test_setup', 'test_setup'],
        'open': [100.0, 50.0],
        'close': [110.0, 55.0],
        'high': [115.0, 60.0],
        'low': [100.0, 50.0],
        'metric': ['sma', 'sma'],
        'value': [120.0, 70.0]})

    log_df = pd.DataFrame({
        'time': [date_today, date_tomorrow],
        'ticker': ['test_setup', 'test_setup'],
        'activity': ['activity', 'activity'],
        'price': [20.0, 30.0],
        'remarks': ['hello', 'world']})

    write_to_db('tickerdata', ticker_df)
    write_to_db('activitylog', log_df)

#    read_ticker_df = read_from_tickerdata('test_setup', 'sma', date_today, date_tomorrow, timedelta(days=1).total_seconds())
#    read_log_df = read_from_activitylog('test_setup', 'activity')
#
#    print()
#    print(ticker_df)
#    print(read_ticker_df)
#
#    print()
#    print(log_df)
#    print(read_log_df)
#    print()

if __name__ == '__main__':
    setup()
    test_setup()
