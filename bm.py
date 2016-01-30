"""Requests and inserts data into Beeminder."""

import json, logging
import requests
from datetime import date, timedelta, datetime
from collections import namedtuple

import db


BMDatapoint = namedtuple("BMDatapoint", "id, value")

DT_FORMAT = '%Y-%m-%d %H:%M:%S'

class BeemAPI(object):
    """A wrapper class for Beeminder's API requests."""

    URL = 'https://www.beeminder.com/api/v1'

    def __init__(self, bm_goal_url):
        self.auth_token = db.get_parameter('bm_api_token')
        self.user = db.get_parameter('bm_user_name')
        self.goal = bm_goal_url

    def is_updated(self):
        """Returns if bm user was updated at all since last run."""

        last_updated = 0

        try:
            with open('updated_at', 'r') as updated_file:
                last_updated = int(updated_file.readline())
        except FileNotFoundError:
            with open('updated_at', 'w') as updated_file:
                updated_file.write(str(last_updated))

        url = BeemAPI.URL
        url += '/users/' + str(self.user) + '.json'
        params = {'auth_token':self.auth_token}

        response = requests.get(url, params=params)

        logging.debug(json.dumps(response.json(), sort_keys=True,
                                 indent=4, separators=(',', ':')))

        updated_at = int(response.json()['updated_at'])

        logging.debug('updated_at is: ' + str(updated_at))

        if last_updated >= updated_at:
            logging.debug('last_updated >= updated_at')
            return False
        else:
            logging.debug('last_updated < updated_at')
            with open('updated_at', 'w') as updated_file:
                updated_file.write(str(updated_at))
            return True



    def get_data(self, datapoint_date):
        """Requests and returns the datapoint for a given date from Beeminder.

        Keyword arguments:
        datapoint_date -- date to request the data for (no default)
        Raises:
        AttributeError -- on incorrect date argument
        """

        try:
            datapoint_date = datapoint_date.isoformat().replace('-', '')
            logging.debug(datapoint_date)


            url = BeemAPI.URL
            url += '/users/' + str(self.user)
            url += '/goals/' + str(self.goal)
            url += '/datapoints.json'

            params = {'auth_token':self.auth_token}


            response = requests.get(url, params=params)

            logging.debug(json.dumps(response.json(), sort_keys=True,
                                     indent=4, separators=(',', ':')))

            result = None
            for sth in response.json():
                if sth['daystamp'] == datapoint_date:
                    logging.debug('datapoints id is: ' + str(sth['id']))
                    logging.debug('datapoint is: ' + str(sth['daystamp']) +
                                  ' : ' + str(sth['value']))
                    result = BMDatapoint(sth['id'], sth['value'])

            return result
        except AttributeError as ex:
            logging.error(ex)
            raise

    def insert(self, data, debug=False):
        """Creates a new datapoint with the provided value.

        Returns the new datapoint's id.
        """

        url = BeemAPI.URL
        url += '/users/' + str(self.user)
        url += '/goals/' + str(self.goal)
        url += '/datapoints.json'

        now = datetime.strftime(datetime.utcnow(), DT_FORMAT) + ' UTC'
        params = {'auth_token':self.auth_token, 'value':data,
                  'comment':'Inserted by TogglToBM on ' + now}

        if not debug:
            response = requests.post(url, params=params)
            logging.debug('Inserting... Response:')
            logging.debug(json.dumps(response.json(), sort_keys=True,
                          indent=4, separators=(',', ':')))

            return str(response.json()['id'])

        else:
            logging.debug('If not debug, would post: requests.post(' +
                          str(url) +') with params=' + str(params))


    def update(self, datapoint_id, data, debug=False):
        """Updates an existing datapoint with new value."""

        url = BeemAPI.URL
        url += '/users/' + str(self.user)
        url += '/goals/' + str(self.goal)
        url += '/datapoints/' + str(datapoint_id) + '.json'

        now = datetime.strftime(datetime.utcnow(), DT_FORMAT) + ' UTC'
        params = {'auth_token':self.auth_token, 'value':data,
                  'comment':'Updated by TogglToBM on ' + now}

        if not debug:
            response = requests.put(url, params=params)
            logging.debug('Updating... Response:')
            logging.debug(json.dumps(response.json(), sort_keys=True,
                          indent=4, separators=(',', ':')))
        else:
            logging.debug('If not debug, would put: requests.put(' +
                          str(url) +') with params=' + str(params))


if __name__ == '__main__':

    LOG_DIR = './logs/test/bm_'
    LOG_DATE = str(date.today().isoformat().replace('-', ''))
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                         level=logging.DEBUG, format=LOG_FORMAT)

    DAY = date.today() - timedelta(days=1)

    BM = BeemAPI()

    BM_DATA = BM.get_data(DAY)
    logging.debug("data from bm: " + str(BM_DATA))
    logging.debug("data from bm: " + str(BM_DATA.id))
    logging.debug("data from bm: " + str(BM_DATA.value))

    BM_DATA = BM.get_data('incorrect date')

    BM.is_updated()
