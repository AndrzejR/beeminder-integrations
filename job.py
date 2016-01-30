"""This is the main executable meant to be scheduled."""

import logging
import bm, toggl, db
from datetime import date

DEBUG = True # set to True not to insert or update anything in Beeminder

LOG_DIR = './logs/'
LOG_DATE = str(date.today().isoformat().replace('-', ''))
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                    level=logging.DEBUG, format=LOG_FORMAT)

logging.info("****************** Starting a new run ******************")

TODAY = date.today()

TOGGL_DATA = toggl.get_data(TODAY)
logging.debug("Today's data from toggl: " + str(TOGGL_DATA))

# add: is the toggl data different than last time?
if TOGGL_DATA != 0:

    BM = bm.BeemAPI()

    DATAPOINT_ID = db.load_dp_id(TODAY)

    # we don't have a datapoint id for the day, insert needed
    if DATAPOINT_ID is None:
        logging.debug('datapoint_id is None. Will insert into bm.')
        NEW_DATAPOINT_ID = BM.insert(data=TOGGL_DATA, debug=DEBUG)
        db.write_dp_id(NEW_DATAPOINT_ID, TODAY)
    # we have a datapoint id, update
    else:
        logging.debug('Updating datapoint ' + str(DATAPOINT_ID))
        BM.update(datapoint_id=DATAPOINT_ID, data=TOGGL_DATA, debug=DEBUG)


else:
    logging.info("No data for toggl for today.")
