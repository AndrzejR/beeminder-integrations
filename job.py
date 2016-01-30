"""This is the main executable meant to be scheduled."""

import logging
import bm, toggl, db, habitica
from datetime import date

DEBUG = False # set to True not to insert or update anything in Beeminder

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

    BM = bm.BeemAPI('togglproductivity2015')

    DATAPOINT_ID = db.load_dp_id(TODAY, 'togglproductivity2015')

    # we don't have a datapoint id for the day, insert needed
    if DATAPOINT_ID is None:
        logging.debug('datapoint_id is None. Will insert into bm.')
        NEW_DATAPOINT_ID = BM.insert(data=TOGGL_DATA, debug=DEBUG)
        db.write_dp_id(NEW_DATAPOINT_ID, TODAY, 'togglproductivity2015')
    # we have a datapoint id, update
    else:
        logging.debug('Updating datapoint ' + str(DATAPOINT_ID))
        BM.update(datapoint_id=DATAPOINT_ID, data=TOGGL_DATA, debug=DEBUG)


else:
    logging.info("No data for toggl for today.")


HB = habitica.HabitAPI()

# if no datapoint - insert complete=1 incomplete=0
# if not synchronized update as above
# be extra careful about date differences

for daily in db.get_active_dailies():
    completed = int(HB.is_daily_completed(daily[0]))
    logging.debug('completed: ' + str(completed))
    DATAPOINT = db.load_dp(TODAY, daily[1])
    BM = bm.BeemAPI(daily[1])
    if DATAPOINT is None:
        NEW_DATAPOINT_ID = BM.insert(completed, debug=DEBUG)
        if NEW_DATAPOINT_ID is not None:
            db.write_dp_id(NEW_DATAPOINT_ID, TODAY, daily[1], completed)
    elif DATAPOINT[1] != completed:
        BM.update(DATAPOINT[0], completed, debug=DEBUG)
        db.update_dp(DATAPOINT[0], completed)

    # print(BM.get_data(TODAY))
    
    #NEW_DATAPOINT_ID = BM.insert(data=TOGGL_DATA, debug=DEBUG)
    # db.write_dp_id()

    # print(daily_id[0] + ': ' + str(HB.is_daily_completed(daily_id[0])))

