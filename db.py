"""This module is intended to save datapoints (or more) to the db."""

import sqlite3
import logging
from datetime import date

DATABASE_FILE = 'bm_in.db'
CONNECTION = sqlite3.connect(DATABASE_FILE)

def load_dp_id(datapoint_date):
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
        dp_t = datapoint_date,
        cur.execute('select id from bm_datapoint where daystamp=?', dp_t)
        datapoint_id = cur.fetchone()
        logging.debug('datapoint_id from db: ' + str(datapoint_id))
        return datapoint_id[0]

    except Exception as exc:
        logging.error(exc)

def write_dp_id(datapoint_id, datapoint_date, value=0):
    """Writes the datapoint id for the given date into the db."""
    try:
        cur = CONNECTION.cursor()
        datapoint = (datapoint_id, value, datapoint_date)
        logging.debug(datapoint)
        cur.execute("""insert into bm_datapoint
                    (id, value, daystamp)
                    values
                    (?,?,?)"""
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
                    (id, value, daystamp)
                    values
                    ('abc1', 10, '2015-05-16')
                    """)
        cur.execute("""insert into bm_datapoint
                    (id, value, daystamp)
                    values
                    ('abc2', 5, '2015-05-01')
                    """)
        CONNECTION.commit()

        TODAY = date.today()
        logging.debug(TODAY)
        logging.debug("today's dp: " + str(load_dp_id(TODAY)))

        TEST_DATE = date(2015, 5, 1)
        logging.debug("2015-05-01's dp: " + str(load_dp_id(TEST_DATE)))

    finally:
        cur.execute("""delete from bm_datapoint
                    where id in ('abc1', 'abc2')""")
        CONNECTION.commit()

    try:
        logging.debug('*** write test ***')
        WRITE_TEST_DATE = date(2015, 1, 13)
        write_dp_id('write_test_1', WRITE_TEST_DATE, 13)
        logging.debug("write test dp: " + str(load_dp_id(WRITE_TEST_DATE)))
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