import requests
import pandas as pd
import polars as pl

airtable_key = 'patEA62AjIZq9Ad3N.7b067c9a8a47cd1f036288606e5e26f1da1748323fba0b6b3951610596fb0002' 
base_id = 'appqiHo29pLLU6RDC'
orgs_table_id = 'tblqoitqeXyTPwU8i/'
view_id = 'viw6rspeIZ8v1IWXt'
headers = {'Authorization': f'Bearer {airtable_key}'}


url = f'https://api.airtable.com/v0/{base_id}/{orgs_table_id}'

def make_request():
    airtable_key = 'patEA62AjIZq9Ad3N.7b067c9a8a47cd1f036288606e5e26f1da1748323fba0b6b3951610596fb0002' 
    base_id = 'appqiHo29pLLU6RDC'
    orgs_table_id = 'tblqoitqeXyTPwU8i/'
    view_id = 'viw6rspeIZ8v1IWXt' #optional
    headers = {'Authorization': f'Bearer {airtable_key}'}
    url = f'https://api.airtable.com/v0/{base_id}/{orgs_table_id}'
    response = requests.get(url, headers=headers)
    return response

def get_first_page():
    response = make_request()
    records = response.json()['records']
    records_list = [record['fields'] for record in records]
    columns = ['name', 'alternate_name', 'x-status', 'x-verification', 'Service Area', 'phones', 'url', 'description', 'services', 'email', 'locations', 'x-website rating', 'x-status_last_modified', 'id']
    df = pd.DataFrame(records_list, columns=columns)
    return df
#df.to_csv('orgs_connect211.csv', index=False, header=True)

# p -> page
def get_core():
    columns = ['name', 'alternate_name', 'x-status', 'x-verification', 'Service Area', 'phones', 'url', 'description', 'services', 'email', 'locations', 'x-website rating', 'x-status_last_modified', 'id']
    df = get_first_page()
    response = make_request()
    records = response.json()
    list_of_dfs = [df]
    offset = records['offset']
    base_url = url
    offset_url = f'?offset={offset}'
    p_url = base_url + offset_url
    while True:
        p_response = requests.get(p_url, headers=headers)
        p_json = p_response.json()
        p_records = p_json['records']
        p_records_list = [record['fields'] for record in p_records]
        p_df = pd.DataFrame(p_records_list, columns=columns)
        list_of_dfs.append(p_df)
        if 'offset' in p_json.keys():
            offset = p_json['offset']
            offset_url = f'?offset={offset}'
            p_url = base_url + offset_url
        else:
            break
    data = pd.concat(list_of_dfs)
    return data


# def get_x_verification(core_dict, reduced_x_verification_dict):
#     for record in core_dict:
#         if 'x-verification' in record.keys():
#             org_id = record['id']
#             x_verifications = reduced_x_verification_dict[org_id]
#             record['x-verification'] = x_verifications
#         else:
#             record['x-verification'] = ''
#     return core_dict