import json

from pipedrive_adapter import fetch_deals
from datetime import datetime

# from code import interact

def normalize_values(values):
    result = {
        'total_created' : 0.0,
        'total_won' : 0.0,
        'total_target' : 768000.00,
        'forecast' : 0.0,
    }
    for vals in values:
        for e in vals['data']:
            # interact(local=dict(globals(), **locals()))
            if is_current_year_and_month(e['add_time']):
                result['total_created'] += e['value']
    
            if e['status'] == 'won':
                if is_current_year_and_month(e['won_time']):
                    result['total_won'] += e['value']
    
            elif e['status'] == 'open' and e['expected_close_date'] != None:
                if is_current_year_and_month(e['expected_close_date']):
                    result['forecast'] += (e['value'] * (e['probability'] or 0.1))
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

def is_current_month(date_string):
    current_month = str(datetime.today().month)

    return date_string.split(' ')[0].split('-')[1] == current_month

def is_current_year(date_string):
    current_year = str(datetime.today().year)

    return date_string.split(' ')[0].split('-')[0] == current_year

def is_current_year_and_month(date_string):
    return is_current_year(date_string) and is_current_month(date_string)
