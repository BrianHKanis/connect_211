import requests
import pandas as pd
import time
from build_tables.core_tables import organizations, services, locations, service_at_location
from build_tables import tables
import json

all_tables = tables.build_all()