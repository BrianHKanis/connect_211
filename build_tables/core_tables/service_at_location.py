from build_tables.tables import build_dict, reduce_dict, reduce_dict_multiple_values
from build_tables.tables import airtable_key, base_id, table_id_dict, headers
from build_tables.hsds_columns import services_at_location_columns

required = ['id']


def delete_or_rename_columns(core_dict):
    for record in core_dict:
        if 'locations' in record.keys():
            record['location'] = record['locations']
    for record in core_dict:
        for k, v in list(record.items()):
            if k not in services_at_location_columns:
                del record[k]
    return core_dict

def add_required_if_missing(core_dict):
    for record in core_dict:
        if 'id' not in record.keys():
            record['id'] = ''
    return core_dict

def get_phones(core_dict, reduced_phone_dict):
    for record in core_dict:
        if 'phone_ids' in record.keys():
            phone_ids = record['phone_ids']
            phone_numbers = [reduced_phone_dict[phone_id] for phone_id in phone_ids]
            record['phones'] = phone_numbers
    return core_dict

def get_locations(core_dict, reduced_location_dict):
    for record in core_dict:
        if 'location' in record.keys():
            location_ids = record['location']
            locations = [reduced_location_dict[id] for id in location_ids]
            if len(locations) > 1:
                record['location'] = locations
            else:
                record['location'] = locations[0]
    return core_dict

def get_addresses(core_dict, reduced_addresses_dict):
    for record in core_dict:
        if 'address' in record.keys():
            physical_address_ids = record['address']
            if len(physical_address_ids) > 1:
                addresses = [reduced_addresses_dict[id] for id in physical_address_ids] 
                record['address'] = addresses 
            else:
                address = reduced_addresses_dict[physical_address_ids[0]]
                record['address'] = address   
    return core_dict

def complete_table():
    service_records = build_dict('services')
    services_hsds = delete_or_rename_columns(service_records)
    phone_records = build_dict('phones')
    location_records = build_dict('locations')
    address_records = build_dict('physical_addresses')

    reduced_phones = reduce_dict(phone_records, 'id', 'number')
    reduced_addresses = reduce_dict_multiple_values(address_records, 'id', ['address_1', 'x-address_2', 'city'])
    locations_with_addresses = get_addresses(location_records, reduced_addresses) # Extra step to add addresses to locations table
    reduced_locations = reduce_dict_multiple_values(locations_with_addresses, 'id', ['name', 'address'])
    services_with_phones = get_phones(services_hsds, reduced_phones)
    services_with_location = get_locations(services_with_phones, reduced_locations)
    
    return services_with_location

# HSDS 3.0
# "id": ▹{...},
# "service_id": ▹{...},
# "location_id": ▹{...},
# "description": ▹{...},
# "contacts": ▹{...},
# "phones": ▹{...},
# "schedules": ▹{...},
# "location": ▹{...},
# "attributes": ▹{...},
# "metadata": ▹{...}


# Airtable
# ['name', 'url', 'taxonomy', 'description', 'application_process', 'organizations',
# 'id', 'y-org status', 'organization_ids', 'taxonomy_ids', 'email', 'phones', 'fees',
# 'phone_ids', 'locations', 'address', 'location_ids', 'alternate_name', 'contacts',
# 'status', 'schedule', 'schedule_ids', 'interpretation_services', 'programs',
# 'accreditations', 'wait_time', 'licenses']