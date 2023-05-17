import requests
import pandas as pd

airtable_key = 'patEA62AjIZq9Ad3N.7b067c9a8a47cd1f036288606e5e26f1da1748323fba0b6b3951610596fb0002' 
base_id = 'appqiHo29pLLU6RDC'
orgs_table_id = 'tblqoitqeXyTPwU8i/'
view_id = 'viw6rspeIZ8v1IWXt'
headers = {'Authorization': f'Bearer {airtable_key}'}
phones_table_id = 'tblvSTMIx5OJBnV2m'
x_status_table_id = 'tblhWvHJVmlgpIdVc'
locations_table_id = 'tblupy32maGd0av6I'
phone_id = 'rec0lQkb6q667eb1u'

url = f'https://api.airtable.com/v0/{base_id}/{orgs_table_id}'

response = requests.get(url, headers=headers)
records_json = response.json()
records = response.json()['records']
records_list = [record['fields'] for record in records]
columns = ['name', 'alternate_name', 'x-status', 'x-verification', 'Service Area', 'phones', 'url', 'description', 'services', 'email', 'locations', 'x-website rating', 'x-status_last_modified', 'id']
df = pd.DataFrame(records_list, columns=columns)
# df.to_csv('orgs_connect211.csv', index=False, header=True)

def get_phones(dataframe):
    phones = dataframe.to_dict()['phones']
    for k, v in phones.items():
        if type(phones[k]) == list:
            phone_nums = []
            phone_ids = phones[k]
            for phone_id in phone_ids:
                url = f'https://api.airtable.com/v0/{base_id}/{phones_table_id}/{phone_id}'
                response = requests.get(url, headers=headers)
                number = response.json()['fields']['number']
                phone_nums.append(number)
            if len(phone_nums) != 1:
                phones[k] = phone_nums
            else:
                phones[k] = phone_nums[0]
    return phones

def get_x_status(dataframe):
    x_status = dataframe.to_dict()['x-verification']
    for k, v in x_status.items():
        if type(x_status[k]) == list:
            x_status_list = []
            x_status_ids = x_status[k]
            for x_id in x_status_ids:
                url = f'https://api.airtable.com/v0/{base_id}/{x_status_table_id}/{x_id}'
                response = requests.get(url, headers=headers)
                task = response.json()['fields']['Task']
                x_status_list.append(task)
            x_status[k] = x_status_list
    return x_status

def get_locations(dataframe):
    locations = dataframe.to_dict()['locations']
    for k, v in locations.items():
        if type(locations[k]) == list:
            actual_locations = []
            location_ids = locations[k]
            for location_id in location_ids:
                url = f'https://api.airtable.com/v0/{base_id}/{locations_table_id}/{location_id}'
                response = requests.get(url, headers=headers)
                loc = response.json()['fields']['name']
                actual_locations.append(loc)
            locations[k] = actual_locations
    return locations

def get_services(dataframe):
    pass
# df_dict = df.to_dict()
# with_phones_dict = get_phones(df)
# with_x_dict = get_x_status(df)
# with_locs_dicts = get_locations(df)

# df_dict['phones'] = with_phones_dict
# df_dict['x-verification'] = with_x_dict
# df_dict['locations'] = with_locs_dicts
# new_df = pd.DataFrame(df_dict)
