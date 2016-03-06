"""This is the main executable of the subscriber job.
Gets the data from the DCM and upserts it into Beeminder.
"""

import logging
import db, bm
from datetime import date, timedelta
from time import sleep

DEBUG = True # set to True not to insert or update anything in Beeminder

LOG_DIR = './logs/subscriber_'
LOG_DATE = str(date.today().isoformat().replace('-', ''))
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                    level=logging.DEBUG, format=LOG_FORMAT)

logging.info("****************** Starting a new subscriber run ******************")

BM = bm.BeemAPI('togglproductivity2015')

for new_dp in db.get_new_toggl_dcm_datapoints():
	new_datapoint_id = BM.insert(data=new_dp[1]/3600000, debug=DEBUG)
	if new_datapoint_id is not None:
		db.update_toggl_dcm_status(new_dp[0], 2, new_datapoint_id)
	else:
		db.update_toggl_dcm_status(new_dp[0], 9)

for mod_dp in db.get_modified_toggl_dcm_datapoints():
	BM.update(datapoint_id=mod_dp[2], data=mod_dp[1]/3600000, debug=DEBUG)
	db.update_toggl_dcm_status(mod_dp[0], 2, mod_dp[2])
