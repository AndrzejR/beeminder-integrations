"""This module is intended to save datapoints (or more) to the db."""

import sqlite3
import logging
from datetime import date

DATABASE_FILE = 'bm_in.db'
CONNECTION = sqlite3.connect(DATABASE_FILE)

def load_dp_id(datapoint_date, bm_url):
    """Returns the datapoint id for the given date.
    Arguments:
    datapoint_date -- date
    Returns None if there is no datapoint for the given date.
    """

    if not isinstance(datapoint_date, date):
        raise ValueError('Incorrect argument type - datapoint_date.')

    datapoint_id = None
    try:
        logging.debug("received datapoint_date: " + str(datapoint_date))
        cur = CONNECTION.cursor()
        params = (datapoint_date, bm_url)
        cur.execute('select id from bm_datapoint where daystamp=? and bm_url=?', params)
        datapoint_id = cur.fetchone()
        logging.debug('datapoint_id from db: ' + str(datapoint_id))
        return datapoint_id[0]

    except Exception as exc:
        logging.error(exc)


def load_dp(datapoint_date, bm_url):
    """Returns the datapoint for the given date.
    Arguments:
    datapoint_date -- date
    Returns None if there is no datapoint for the given date.
    """

    if not isinstance(datapoint_date, date):
        raise ValueError('Incorrect argument type - datapoint_date.')

    datapoint = None
    try:
        logging.debug("received datapoint_date: " + str(datapoint_date))
        cur = CONNECTION.cursor()
        params = (datapoint_date, bm_url)
        cur.execute('select id, value from bm_datapoint where daystamp=? and bm_url=?', params)
        datapoint = cur.fetchone()
        logging.debug('datapoint from db: ' + str(datapoint))
        return datapoint

    except Exception as exc:
        logging.error(exc)

def update_dp(datapoint_id, value=0):
    """Updates the given datapoint for the given date into the db."""
    try:
        cur = CONNECTION.cursor()
        datapoint = (value, datapoint_id)
        logging.debug(datapoint)
        cur.execute("""update bm_datapoint
                    set value=?
                    where id=?
                    """
                    , datapoint)
        CONNECTION.commit()

    except Exception as exc:
        logging.error(exc)


def write_dp_id(datapoint_id, datapoint_date, bm_url, value=0):
    """Writes the datapoint id for the given date into the db."""
    try:
        cur = CONNECTION.cursor()
        datapoint = (datapoint_id, value, datapoint_date, bm_url)
        logging.debug(datapoint)
        cur.execute("""insert into bm_datapoint
                    (id, value, daystamp, bm_url)
                    values
                    (?,?,?,?)"""
                    , datapoint)
        CONNECTION.commit()

    except Exception as exc:
        logging.error(exc)

def get_parameter(param_name):
    try:
        cur = CONNECTION.cursor()
        cur.execute("""select param_value
                    from parameter
                    where param_name=?"""
                    , (param_name,))
        return cur.fetchone()[0]

    except Exception as exc:
        logging.error(exc)

def get_active_dailies():
    try:
        cur = CONNECTION.cursor()
        cur.execute("""select habitica_id
                    , bm_url
                    from bm_goal_xref
                    where is_active=1""")
        return cur.fetchall()

    except Exception as exc:
        logging.error(exc)

def get_toggl_dcm_datapoint(dp_date):
    try:
        cur = CONNECTION.cursor()
        cur.execute("""select toggl_ms
                    , status
                    from dcm_toggl_datapoint
                    where toggl_date = ?"""
                    , (dp_date,))
        return cur.fetchone()

    except Exception as exc:
        logging.error(exc)

def insert_toggl_dcm(date_to_sync, currently_in_toggl):
    try:
        cur = CONNECTION.cursor()
        cur.execute("""insert into dcm_toggl_datapoint
                    ( toggl_ms
                    , status
                    , toggl_date)
                    values 
                    (?, 1, ?)
                    """
                    , (currently_in_toggl, date_to_sync))
        CONNECTION.commit()

    except Exception as exc:
        print(exc)

def update_toggl_dcm(date_to_sync, currently_in_toggl):
    try:
        cur = CONNECTION.cursor()
        cur.execute("""update dcm_toggl_datapoint
                    set toggl_ms = ?
                    , status = 3
                    where toggl_date = ?
                    """
                    , (currently_in_toggl, date_to_sync))
        CONNECTION.commit()

    except Exception as exc:
        print(exc)

def get_new_toggl_dcm_datapoints():
    try:
        cur = CONNECTION.cursor()
        cur.execute("""select toggl_date
                    , toggl_ms
                    from dcm_toggl_datapoint
                    where status = 1""")
        return cur.fetchall()

    except Exception as exc:
        logging.error(exc)

def get_modified_toggl_dcm_datapoints():
    try:
        cur = CONNECTION.cursor()
        cur.execute("""select toggl_date
                    , toggl_ms
                    , bm_id
                    from dcm_toggl_datapoint
                    where status = 3""")
        return cur.fetchall()

    except Exception as exc:
        logging.error(exc)

def update_toggl_dcm_status(toggl_date, status, bm_id=None):
    try:
        cur = CONNECTION.cursor()
        cur.execute("""update dcm_toggl_datapoint
                    set status = ?
                    , bm_id = ?
                    where toggl_date = ?
                    """
                    , (status, bm_id, toggl_date))
        CONNECTION.commit()

    except Exception as exc:
        print(exc)

if __name__ == '__main__':

    LOG_DIR = './logs/test/db_'
    LOG_DATE = str(date.today().isoformat().replace('-', ''))
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                         level=logging.DEBUG, format=LOG_FORMAT)

    try:
        logging.debug('*** read test ***')
        cur = CONNECTION.cursor()
        cur.execute("""insert into bm_datapoint
                    (id, value, daystamp, bm_url)
                    values
                    ('abc1', 10, '2016-01-30', 'test_url')
                    """)
        cur.execute("""insert into bm_datapoint
                    (id, value, daystamp, bm_url)
                    values
                    ('abc2', 5, '2015-05-01', 'test_url')
                    """)
        CONNECTION.commit()

        TODAY = date.today()
        logging.debug(TODAY)
        logging.debug("today's dp: " + str(load_dp_id(TODAY, 'test_url')))

        TEST_DATE = date(2015, 5, 1)
        logging.debug("2015-05-01's dp: " + str(load_dp_id(TEST_DATE, 'test_url')))

    finally:
        cur.execute("""delete from bm_datapoint
                    where id in ('abc1', 'abc2')""")
        CONNECTION.commit()

    try:
        logging.debug('*** write test ***')
        WRITE_TEST_DATE = date(2015, 1, 13)
        write_dp_id('write_test_1', WRITE_TEST_DATE, value=13, bm_url='test_url')
        logging.debug("write test dp: " + str(load_dp_id(WRITE_TEST_DATE, 'test_url')))
    finally:
        cur = CONNECTION.cursor()
        cur.execute("""delete from bm_datapoint
                    where id in ('write_test_1')""")
        CONNECTION.commit()

    try:
        cur = CONNECTION.cursor()
        cur.execute("""insert into parameter
                    (param_name, param_value)
                    values
                    ('test_param', 'test_value')""")
        print(get_parameter('test_param'))
    finally:
        cur = CONNECTION.cursor()
        cur.execute("""delete from parameter
                    where param_name in ('test_param')""")
        CONNECTION.commit()

    print("***get_active_dailies***")
    print(get_active_dailies())
