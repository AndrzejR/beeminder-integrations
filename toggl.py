"""Gets the data from Toggl."""

import requests
import json
import logging
from datetime import date, timedelta

import db

def get_workspaces():
    api_token = db.get_parameter('toggl_api_token')
    user_agent = db.get_parameter('toggl_user_agent')
    payload = {'user_agent':user_agent}
    response = requests.get('https://www.toggl.com/api/v8/workspaces',
                     auth=(api_token, 'api_token'), params=payload)
    return json.dumps(response.json())    

def get_data(datapoint_date):
    """Requests summary time for a given date and returns in hours."""
    api_token = db.get_parameter('toggl_api_token')
    user_agent = db.get_parameter('toggl_user_agent')
    workspace_id = db.get_parameter('toggl_wrkspc_id')

    datapoint_date = datapoint_date.isoformat()

    payload = {'user_agent':user_agent, 'workspace_id':workspace_id,
                 'since':datapoint_date, 'until':datapoint_date,
                 'grouping':'clients', 'subgrouping':'projects'}

    response = requests.get('https://www.toggl.com/reports/api/v2/summary',
                     auth=(api_token, 'api_token'), params=payload)

    logging.debug(str(json.dumps(response.json(), sort_keys=True,
                                 indent=4, separators=(',', ':'))))

    total_grand_ms = response.json()['total_grand']

    logging.debug(str(datapoint_date) + ':' + str(total_grand_ms))

    return total_grand_ms

def get_data_for_range(since, until):
    """Requests summary time for a date range per day.
    Turns out Toggl currently does not support such format.
    """
    api_token = db.get_parameter('toggl_api_token')
    user_agent = db.get_parameter('toggl_user_agent')
    workspace_id = db.get_parameter('toggl_wrkspc_id')

    since, until = since.isoformat(), until.isoformat()

    payload = {'user_agent':user_agent, 'workspace_id':workspace_id,
                 'since':since, 'until':until,
                 'grouping':'clients', 'subgrouping':'projects'}

    response = requests.get('https://www.toggl.com/reports/api/v2/summary',
                     auth=(api_token, 'api_token'), params=payload)

    logging.debug(str(json.dumps(response.json(), sort_keys=True,
                                 indent=4, separators=(',', ':'))))

    # # total_grand_ms = response.json()['total_grand']

    # # if total_grand_ms is not None:
    # #     total_grand_hours = response.json()['total_grand']/3600000
    # # else:
    # #     total_grand_hours = 0

    # logging.debug(str(datapoint_date) + ':' + str(total_grand_hours))

    return None

if __name__ == "__main__":

    LOG_DIR = './logs/test/toggl_'
    LOG_DATE = str(date.today().isoformat().replace('-', ''))
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=LOG_DIR + LOG_DATE + '.log',
                         level=logging.DEBUG, format=LOG_FORMAT)

    # print(get_workspaces())
    TODAY = date.today()
    # get_data(TODAY)
    
    get_data_for_range(TODAY-timedelta(days=7), TODAY)
