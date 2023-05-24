import requests
import pandas as pd
import time
from build_tables.core_tables import organizations, services, locations, service_at_location
from build_tables import tables
import json

# Locations
start = time.time()
locations_dicts = locations.complete_table()
stop = time.time()
locations_total = stop - start
print('locations: ' + str(locations_total))



# Service at Location
start = time.time()
services_at_location_dicts = service_at_location.complete_table(locations_dicts)
stop = time.time()
service_at_location_total = stop - start
print('service at location: ' + str(service_at_location_total))



# Organizations
start = time.time()
organizations_dicts = organizations.complete_table(locations_dicts)
stop = time.time()
organizations_total = stop - start
print('organizations: ' + str(organizations_total))



# Services
start = time.time()
services_dicts = services.complete_table(organizations_dicts, services_at_location_dicts)
stop = time.time()
services_total = stop - start
print('services: ' + str(stop-start))




# Total Time
grand_total = organizations_total + services_total + locations_total + service_at_location_total
print('Total: ' + str(grand_total))








# Export
print('')
start = time.time()
with open('data/location.json', 'w') as l_json:
    json.dump(locations_dicts, l_json, indent=4, sort_keys=True)
with open('data/service_at_location.json', 'w') as sal_json:
    json.dump(services_at_location_dicts, sal_json, indent=4, sort_keys=True)
with open('data/organization.json', 'w') as o_json:
    json.dump(organizations_dicts, o_json, indent=4, sort_keys=True)
with open('data/service.json', 'w') as s_json:
    json.dump(services_dicts, s_json, indent=4, sort_keys=True)
end = time.time()
print('Export: ' + str(end-start))