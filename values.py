import json

from pipedrive_adapter import fetch_deals
from datetime import datetime
from constants import pd_keys

from code import interact

def normalize_values(values):
    pd_probability_key = pd_keys['probability']
    result = {
        'aaa' : {
            'total_created' : 0.0,
            'total_won' : 0.0,
            'total_target' : 768000.00,
            'total_expected' : 0.0,
        },
        'bbb' : {
            'total_created' : 0.0,
            'total_won' : 0.0,
            'total_target' : 768000.00,
            'total_expected' : 0.0,
        },
        'ccc' : {
            'total_created' : 0.0,
            'total_won' : 0.0,
            'total_target' : 768000.00,
            'total_expected' : 0.0,
        }
    }
    for vals in values:
        for e in vals['data']:
# ===================================================================================================
# PREVIOUS MONTH
            # interact(local=dict(globals(), **locals()))
            if is_month(e['add_time'], 'aaa'):
                result['aaa']['total_created'] += e['value']

            if e['status'] == 'won':
                if is_month(e['won_time'], 'aaa'):
                    result['aaa']['total_won'] += e['value']
# ===================================================================================================
# CURRENT MONTH
            if is_month(e['add_time'], 'bbb'):
                result['bbb']['total_created'] += e['value']

            if e['status'] == 'won':
                if is_month(e['won_time'], 'bbb'):
                    result['bbb']['total_won'] += e['value']

            if e['status'] == 'open' and e['expected_close_date'] != None:
                # interact(local=dict(globals(), **locals()))
                if is_month(e['expected_close_date'], 'bbb'):
                    result['bbb']['total_expected'] += (e['value'] * ((e[pd_probability_key] or 10) / 100.00))
# ===================================================================================================
# FOLLOWING MONTH
            if is_month(e['add_time'], 'ccc'):
                result['ccc']['total_created'] += e['value']

            if e['status'] == 'won':
                if is_month(e['won_time'], 'ccc'):
                    result['ccc']['total_won'] += e['value']

            if e['status'] == 'open' and e['expected_close_date'] != None:
                if is_month(e['expected_close_date'], 'ccc'):
                    result['ccc']['total_expected'] += (e['value'] * ((e[pd_probability_key] or 10) / 100.00))
    return result

def stats(department):
    items_in_collection = True
    start_of_range = 0
    raw_values = []

    while items_in_collection:
        pd_response_json = json.loads(
            fetch_deals(department, start_of_range).read().decode('utf-8')
        )
        raw_values.append(
            pd_response_json
        )
        start_of_range += 100
        items_in_collection = pd_response_json['additional_data']['pagination']['more_items_in_collection']


    normalized_values = normalize_values(raw_values)
    return normalized_values


def calculate_stats(**kwargs):
    department = kwargs['department']

    values = stats(department)

    return values

def is_month(date_string, expected_month):
    expected_month_mapping = {
        'bbb' : 0,
        'ccc' : 1,
        'aaa' : -1,
    }

    current_year = datetime.today().year

    # interact(local=dict(globals(), **locals()))

    requested_month = get_month_string(expected_month_mapping[expected_month])
    if expected_month == 'aaa' and get_month_string(expected_month_mapping['bbb']) == "1":
        requested_year = str(current_year + expected_month_mapping[expected_month])
    else:
        requested_year = str(current_year)

    year, month, _day = date_string.split(' ')[0].split('-')

    return year == requested_year and month == requested_month

def get_month_string(expected_month_factor):
    months = [i for i in range(1,13)]

    current_month = datetime.today().month
    current_month_index = months.index(current_month)
    expected_month = months[current_month_index + expected_month_factor]
    
    return str(expected_month)