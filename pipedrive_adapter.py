import os
from urllib.request import urlopen

from code import interact

def full_url(department, start):
    api_host = os.environ.get('PD_API_HOST')
    api_token = os.environ.get('PD_API_TOKEN')

    if department == 'b2c':
        filter_id = os.environ.get('PD_B2C_DEALS_FILTER_ID')
    elif department == 'b2b':
        filter_id = os.environ.get('PD_B2B_DEALS_FILTER_ID')

    entity = 'deals'
    pd_probability_key = 'cb7ce7922d9146c1fc9bca28bb8fcc9b91f2ebc0'
    relevant_attrs = '(user_id,value,status,won_time,add_time,expected_close_date,%s)' % pd_probability_key

    url = api_host + '/' + entity + ':' + relevant_attrs + '?filter_id=' + filter_id + '&status=all_not_deleted' + '&start=' + str(start) + '&api_token=' + api_token

    return url

def fetch_deals(department, start):
    try:
        deal_response = urlopen(
            full_url(department, start)
        )
    except Exception as e:
        deal_response = None
        print("Could not fetch data!")
        print(e)
    return deal_response