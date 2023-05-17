# string = 'name,alternate_name,x-status,x-verification,Service Area,phones,url,description,services,email,locations,x-website rating,x-status_last_modified,id'
# columns = string.split(',')
# print(columns)
from csv import reader

with open('organizations-Grid view.csv', 'r') as readObj:
    csvReader = reader(readObj)
    headers = next(csvReader)

# To SQL table format
# for header in headers:
#     print(header + ' VARCHAR,')

#Column names with space and comma
for header in headers:
    print(header, end=', ')

# print(headers)










# Select list of dictionaries in a loop
# pd.read_json
# to_csv


# With Airscraper using shared view (No Authentification)
# from airscraper import AirScraper

# client = AirScraper([url])
# data = client.get_table().text

# # print the result
# print(data)

# # save as file
# with open('data.csv','w') as f:
#   f.write(data)

# # use it with pandas
# from io import StringIO
# import pandas as pd

# df = pd.read_csv(StringIO(data), sep=',')
# df.head()



# Using Regex to create re-create download link of csv file (What Airscraper does)
# view_id = re.search(r"(viw[a-zA-Z0-9]+)", str(script)).group(1)
# access_policy = re.search(r"accessPolicy=([a-zA-Z0-9%*]+)", str(script)).group(1)
# app_id = re.search(r"\"x-airtable-application-id\":\"(app[a-zA-Z0-9]+)", str(script)).group(1)