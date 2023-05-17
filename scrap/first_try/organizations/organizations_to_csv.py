import requests
import pandas as pd

airtable_key = 'patEA62AjIZq9Ad3N.7b067c9a8a47cd1f036288606e5e26f1da1748323fba0b6b3951610596fb0002' 
base_id = 'appqiHo29pLLU6RDC'
table_id = 'tblqoitqeXyTPwU8i/'
view_id = 'viw6rspeIZ8v1IWXt'
headers = {'Authorization': f'Bearer {airtable_key}'}


url = f'https://api.airtable.com/v0/{base_id}/{table_id}'

response = requests.get(url, headers=headers)
#open("HSDS_locations.csv", "wb").write(response.content)
records_json = response.json()
records = response.json()['records']
records_list = [record['fields'] for record in records]
columns = ['name', 'alternate_name', 'x-status', 'x-verification', 'Service Area', 'phones', 'url', 'description', 'services', 'email', 'locations', 'x-website rating', 'x-status_last_modified', 'id']
df = pd.DataFrame(records_list, columns=columns)
df.to_csv('orgs_connect211.csv', index=False, header=True)


# p -> page
list_of_dfs = []
offset = records_json['offset']
base_url = url
offset_url = f'?offset={offset}'
p_url = base_url + offset_url
p_response = requests.get(p_url, headers=headers)
while True:
    p_response = requests.get(p_url, headers=headers)
    p_json = p_response.json()
    p_records = p_json['records']
    p_records_list = [record['fields'] for record in p_records]
    p_df = pd.DataFrame(p_records_list, columns=columns)
    if 'offset' in p_json.keys():
        offset = p_json['offset']
        offset_url = f'?offset={offset}'
        p_url = base_url + offset_url
        with open('orgs_connect211.csv','a') as f:
            df.to_csv(f)
            f.write("\n")
        # list_of_dfs.append(p_df)
    else:
        break

# with open('/Users/brian/connect211/practice/organizations_connect211.csv','a') as f:
#     for df in list_of_dfs:
#         df.to_csv(f)
#         f.write("\n")

# print(list_of_dfs)

# dfs = append_remaining(records_json, columns)
# print(dfs)
# page_2_url = f'https://api.airtable.com/v0/{base_id}/{table_id}?offset=itrILFOYBb1mquqka/recfPcfixvgRYPbpO'
# page_2_response = requests.get(page_2_url, headers=headers)
# page_2_records_json = page_2_response.json()
# page_2_records = page_2_records_json['records']
# page_2_records_list = [record['field'] for record in page_2_records]



# offset = itrYLRYlLRa5m3d9m/recfPcfixvgRYPbpO
# itrILFOYBb1mquqka/recfPcfixvgRYPbpO