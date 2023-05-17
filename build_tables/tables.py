import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

airtable_key = os.getenv('AIRTABLE_KEY') 
base_id = 'appqiHo29pLLU6RDC'
table_id_dict = {'organizations': 'tblqoitqeXyTPwU8i', 'services': 'tbl55axdd1ToQnD8a',
                 'locations': 'tblupy32maGd0av6I', 'phones': 'tblvSTMIx5OJBnV2m',
                 'x-verification': 'tblhWvHJVmlgpIdVc', 'taxonomy_terms': 'tblGdXYo1onpkh7ow',
                 'schedule': 'tblDtGJOo2adZBWui', 'x-taxonomies': 'tbljWxEZPvYL3CmVU',
                 'physical_addresses': 'tblo9O05Tcxuhm5ro', 'contacts': 'tblX4DJEnxDCd3d6e'}
headers = {'Authorization': f'Bearer {airtable_key}'}

def make_request(table_name):
    url = f'https://api.airtable.com/v0/{base_id}/'
    request_url = url + table_id_dict[table_name]
    response = requests.get(request_url, headers=headers)
    return response

def get_first_page(table_name):
    response = make_request(table_name)
    records = response.json()['records']
    records_list = [record['fields'] for record in records]
    columns = ['name', 'alternate_name', 'x-status', 'x-verification', 'Service Area', 'phones', 'url', 'description', 'services', 'email', 'locations', 'x-website rating', 'x-status_last_modified', 'id']
    df = pd.DataFrame(records_list, columns=columns)
    return df

def build_dict(table_name):
    url = f'https://api.airtable.com/v0/{base_id}/{table_id_dict[table_name]}'
    response = make_request(table_name)
    records_json = response.json()
    records_list = records_json['records']
    offset = records_json['offset']
    offset_url = f'/?offset={offset}'
    next_url = url + offset_url
    while True:
        next_response = requests.get(next_url, headers=headers)
        next_json = next_response.json()
        next_records_list = next_json['records']
        records_list.extend(next_records_list)
        if 'offset' in next_json.keys():
            offset = next_json['offset']
            offset_url = f'/?offset={offset}'
            next_url = url + offset_url
        else:
            break
    records = [record['fields'] for record in records_list]
    return records

def reduce_dict(main_dict, key_name, value_name):
    reduced_dict = {}
    for record in main_dict:
        if key_name in record.keys():
            if type(record[key_name]) != list:
                key = record[key_name]
            else:
                key = record[key_name][0]
            if value_name in record.keys():
                value = record[value_name]
            else:
                value = ''
        reduced_dict[key] = value
    return reduced_dict

def reduce_dict_multiple_values(main_dict, key_name, value_names):
    reduced_dict = {}
    for record in main_dict:
        if key_name in record.keys():
            if type(record[key_name]) != list:
                key = record[key_name]
            else:
                key = record[key_name][0]
            values_list = []
            for value_name in value_names:
                if value_name in record.keys():
                    value = record[value_name]
                    value_dict = {value_name: value}
                    values_list.append(value_dict)
        reduced_dict[key] = values_list
    return reduced_dict

def build_dict_with_date_created(table_name):
    url = f'https://api.airtable.com/v0/{base_id}/{table_id_dict[table_name]}'
    response = make_request(table_name)
    records_json = response.json()
    records_list = records_json['records']
    offset = records_json['offset']
    offset_url = f'/?offset={offset}'
    next_url = url + offset_url
    while True:
        next_response = requests.get(next_url, headers=headers)
        next_json = next_response.json()
        next_records_list = next_json['records']
        records_list.extend(next_records_list)
        if 'offset' in next_json.keys():
            offset = next_json['offset']
            offset_url = f'/?offset={offset}'
            next_url = url + offset_url
        else:
            break
    return records_list


# def build_df(table_name):
#     url = f'https://api.airtable.com/v0/{base_id}/{table_id_dict[table_name]}'
#     response = make_request(table_name)
#     df = get_first_page(table_name)
#     records = response.json()
#     list_of_dfs = [df]
#     offset = records['offset']
#     offset_url = f'/?offset={offset}'
#     p_url = url + offset_url
#     while True:
#         p_response = requests.get(p_url, headers=headers)
#         p_json = p_response.json()
#         p_records = p_json['records']
#         p_records_list = [record['fields'] for record in p_records]
#         p_df = pd.DataFrame(p_records_list)
#         list_of_dfs.append(p_df)
#         if 'offset' in p_json.keys():
#             offset = p_json['offset']
#             offset_url = f'/?offset={offset}'
#             p_url = url + offset_url
#         else:
#             break
#     data = pd.concat(list_of_dfs)
#     return data