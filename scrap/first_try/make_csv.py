import requests
import pandas as pd

airtable_key = 'keyUwFxvmOO8PXt5v' 
airtable_id = 'appy9PwmY4NCMIji5'
headers = {'Authorization': f'Bearer {airtable_key}'}

url = f'https://api.airtable.com/v0/{airtable_id}/Connect211_practice'
response = requests.get(url, headers=headers)
records_json = response.json()
records = response.json()['records']
records_list = [record['fields'] for record in records]
columns = ['id', 'organization_id', 'name', 'alternate_name', 'description', 'transportation'
           'latitude', 'longitude']
df = pd.DataFrame(records_list, columns=columns)
# df.to_csv('hsds_locations.csv', index=False, header=True)

# Test for dealing with Null values in longitutde
new_df = df.fillna(000.000000)
new_df.to_csv('hsds_locations_nulls.csv', index=False, header=True)
