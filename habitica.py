"""Gets the data from Habitica."""

import requests
import json
import logging
from datetime import date
import db

def get_data():
    """Gets data"""
    api_token = db.get_parameter('habitica_api_token')
    user_agent = db.get_parameter('habitica_user_id')
    print("user_agent: " + str(user_agent))
    # habit = db.get_parameter('habitica_habit')

    payload = {'x-api-user':user_agent, 'x-api-key':api_token}
    
    response = requests.get('https://habitica.com/api/v2/user/tasks/', headers=payload)

    logging.debug(str(json.dumps(response.json(), sort_keys=True,
                                 indent=4, separators=(',', ':'))))

    print(str(json.dumps(response.json(), sort_keys=True,
                                 indent=4, separators=(',', ':'))))

if __name__ == "__main__":

    LOG_DIR = './'
    LOG_DATE = str(date.today().isoformat().replace('-', ''))
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                         level=logging.DEBUG, format=LOG_FORMAT)

    get_data()
