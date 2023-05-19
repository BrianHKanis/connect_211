import requests
import pandas as pd
import time
import csv
from build_tables.core_tables import organizations, services, locations, service_at_location
from build_tables import tables

# Organizations
start = time.time()
organizations_dicts = organizations.complete_table()
stop = time.time()
organizations_total = stop - start
print('orgs: ' + str(organizations_total))

# Services
start = time.time()
services_dicts = services.complete_table()
stop = time.time()
services_total = stop - start
print('services: ' + str(stop-start))

# Locations
start = time.time()
locations_dicts = locations.complete_table()
stop = time.time()
locations_total = stop - start
print('locations: ' + str(locations_total))

# Service at Location
start = time.time()
services_at_location_dicts = service_at_location.complete_table()
stop = time.time()
service_at_location_total = stop - start
print('service at location: ' + str(service_at_location_total))

# Total Time
grand_total = organizations_total + services_total + locations_total + service_at_location_total
print('Total: ' + str(grand_total))