# With Airscraper using shared view (No Authentification)
from airscraper import AirScraper

password = 'password'
client = AirScraper('https://airtable.com/shrhHi9hFkPNePXgZ/tblUXIdyKGT63xLjc')
data = client.get_table().text

# print the result
print(data)

# # save as file
# with open('data.csv','w') as f:
#   f.write(data)

# # use it with pandas
# from io import StringIO
# import pandas as pd

# df = pd.read_csv(StringIO(data), sep=',')
# df.head()