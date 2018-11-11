import json

from pipedrive_adapter import fetch_deals
from datetime import datetime

from code import interact

def normalize_values(values):
    result = { 'total' : 0.0 }
    for e in values['data']:
        result['total'] += e['value']
    return result

def stats(department):
    items_in_collection = True
    start_of_range = 0
    raw_values = []

    while items_in_collection:
        pd_response_json = json.loads(
            fetch_deals(department).read().decode('utf-8')
        )
        raw_values.append(
            pd_response_json
        )
        start_of_range += 100
        items_in_collection = pd_response_json['additional_data']['pagination']['more_items_in_collection']


    normalized_values = normalize_values(pd_response_json)
    return normalized_values


def calculate_stats(**kwargs):
    department = kwargs['department']

    values = stats(department)

    return values
