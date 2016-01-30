"""Gets the data from Habitica."""

import requests
import json
import logging
from datetime import date
import db

class HabitAPI(object):
    """Wrap the habitica API into an object."""

    URL = 'https://habitica.com/api/v2/'

    def __init__(self):
        self.api_token = db.get_parameter('habitica_api_token')
        self.user_agent = db.get_parameter('habitica_user_id')    

    def get_tasks(self):
        """Gets all tasks."""
        try:
            payload = {'x-api-user':self.user_agent, 'x-api-key':self.api_token}
            
            response = requests.get(HabitAPI.URL + 'user/tasks/', headers=payload)

            logging.debug(str(json.dumps(response.json(), sort_keys=True,
                                         indent=4, separators=(',', ':'))))

            return response.json()
        except Exception as exc:
            logging.error(exc)

    def is_daily_completed(self, daily_id):
        """Returns if the daily is completed today - boolean.
        Other than today's status could be taken from history, however,
        as history is described as causing major performance problems
        on habitica's API page, maybe better not count on it.
        """
        try:
            payload = {'x-api-user':self.user_agent, 'x-api-key':self.api_token}        
            response = requests.get(HabitAPI.URL + 'user/tasks/' + str(daily_id), headers=payload)
            logging.debug(str(json.dumps(response.json(), sort_keys=True,
                                         indent=4, separators=(',', ':'))))
            return response.json()['completed']

        except Exception as exc:
            logging.error(exc)

if __name__ == "__main__":

    LOG_DIR = './'
    LOG_DATE = str(date.today().isoformat().replace('-', ''))
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                         level=logging.DEBUG, format=LOG_FORMAT)

    HB = HabitAPI()
    HB.get_tasks()
    print(HB.is_daily_completed('5b90e6d5-67d4-44c6-86c8-3a0c281d24f9'))


# end result load either true or false into BM at the end of the day
# I need true or false for the specific daily;
# the daily should be configurable - config table with the names, ids, isactive of the mappings
# from the pov of the job: for active job in the config: get today's completed
