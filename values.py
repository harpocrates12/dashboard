import json

from pipedrive_adapter import fetch_deals
from datetime import datetime

# from code import interact

def normalize_values(values):
    current_month = str(datetime.today().month)
    current_year = str(datetime.today().year)

    result = {
        'total_created' : 0.0,
        'total_won' : 0.0,
        'total_target' : 768000.00,
        'forecast' : 0.0,
    }
    for vals in values:
        for e in vals['data']:
            # interact(local=dict(globals(), **locals()))
            if e['add_time'].split(' ')[0].split('-')[1] == current_month:
                    if e['add_time'].split(' ')[0].split('-')[0] == current_year:
                        result['total_created'] += e['value']
    
            if e['status'] == 'won':
                if e['won_time'].split(' ')[0].split('-')[1] == current_month:
                    if e['won_time'].split(' ')[0].split('-')[0] == current_year:
                        result['total_won'] += e['value']
    
            elif e['status'] == 'open' and e['expected_close_date'] != None:
                if e['expected_close_date'].split(' ')[0].split('-')[1] == current_month:
                    if e['expected_close_date'].split(' ')[0].split('-')[0] == current_year:
                        if e['probability'] == None:
                            e['probability'] = 1.0
                        result['forecast'] += (e['value'] * e['probability'])
    return result

def stats(department):
    items_in_collection = True
    start_of_range = 0
    raw_values = []

    while items_in_collection:
        print('Here')
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
