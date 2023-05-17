from pyairtable import Api, Base, Table

airtable_key = 'patEA62AjIZq9Ad3N.7b067c9a8a47cd1f036288606e5e26f1da1748323fba0b6b3951610596fb0002' 
base_id = 'appqiHo29pLLU6RDC'
table_id = 'tblqoitqeXyTPwU8i'
view_id = 'viw6rspeIZ8v1IWXt'
headers = {'Authorization': f'Bearer {airtable_key}'}


url = f'https://api.airtable.com/v0/{base_id}/{table_id}'

api = Api(airtable_key)
api.all(base_id, table_id)

base = Base(airtable_key, base_id)
base.all(table_id)

table = Table(airtable_key, base_id, table_id)
records = table.all()