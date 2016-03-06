"""This is the main executable of the provider job."""

import logging
import toggl, db, habitica
from datetime import date, timedelta
from time import sleep

DATE_RANGE = 3

LOG_DIR = './logs/provider_'
LOG_DATE = str(date.today().isoformat().replace('-', ''))
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                    level=logging.DEBUG, format=LOG_FORMAT)

logging.info("****************** Starting a new provider run ******************")

for DateDelta in range(DATE_RANGE):
	date_to_sync = date.today()-timedelta(days=DateDelta)
	currently_in_toggl = toggl.get_data(date_to_sync)
	currently_in_dcm = db.get_toggl_dcm_datapoint(date_to_sync)
	if not currently_in_dcm:
		db.insert_toggl_dcm(date_to_sync, currently_in_toggl)
	elif currently_in_toggl != currently_in_dcm[0]:
		db.update_toggl_dcm(date_to_sync, currently_in_toggl)
	sleep(2) # horrible hack; as it turns out I can't just get the data grouped per day for a date range
	# and there is a limit of 1 API call per second in Toggl
