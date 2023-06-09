import requests
import pandas as pd
import time
from build_tables.core_tables import organizations, services, locations, service_at_location
from build_tables import tables
import json

all_tables = tables.build_all()

for k, v in all_tables.items():
    with open(f'new_data/{k}.json', 'w') as somejson:
        json.dump(v, somejson, indent=4, sort_keys=True)
