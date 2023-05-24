from build_tables.tables import build_dict, reduce_dict, reduce_dict_multiple_values
from build_tables.tables import airtable_key, base_id, table_id_dict, headers
from build_tables.hsds_columns import services_at_location_columns, locations_columns, address_columns, schedule_columns, phones_columns, contact_columns

required = ['id']

def delete_or_rename_columns(core_dict):
    for record in core_dict:
        if 'locations' in record.keys():
            record['location'] = record['locations']
        if 'schedule' in record.keys():
            record['schedules'] = record['schedule']
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
        if 'phones' in record.keys():
            phone_ids = record['phones']
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

def get_schedules(core_dict, reduced_schedule_dict):
    for record in core_dict:
        if 'schedules' in record.keys():
            schedule_ids = record['schedules']
            schedules = [reduced_schedule_dict[id] for id in schedule_ids] 
            record['schedules'] = schedules
    return core_dict

def get_contacts(core_dict, reduced_contact_dict):
    for record in core_dict:
        if 'contacts' in record.keys():
            contact_ids = record['contacts']
            contacts = [reduced_contact_dict[id] for id in contact_ids] 
            record['contacts'] = contacts
    return core_dict


def complete_table(complete_location_table):
    service_records = build_dict('services')
    services_hsds = delete_or_rename_columns(service_records)
    phone_records = build_dict('phones')
    location_records = complete_location_table
    address_records = build_dict('physical_addresses')
    schedule_records = build_dict('schedule')
    contact_records = build_dict('contacts')

    reduced_schedules = reduce_dict_multiple_values(schedule_records, 'id', schedule_columns)
    reduced_phones = reduce_dict_multiple_values(phone_records, 'id', phones_columns)
    reduced_addresses = reduce_dict_multiple_values(address_records, 'id', address_columns)
    contacts_with_phones = get_phones(contact_records, reduced_phones)
    reduced_contacts = reduce_dict_multiple_values(contacts_with_phones, 'id', contact_columns)

    locations_with_addresses = get_addresses(location_records, reduced_addresses) # Extra step to add addresses to locations table
    reduced_locations = reduce_dict_multiple_values(locations_with_addresses, 'id', locations_columns)
    services_with_phones = get_phones(services_hsds, reduced_phones)
    services_with_location = get_locations(services_with_phones, reduced_locations)
    services_with_schedules = get_schedules(services_with_location, reduced_schedules)
    services_with_contacts = get_contacts(services_with_schedules, reduced_contacts)
    return services_with_contacts

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


# Service (Airtable)
# ['name', 'url', 'taxonomy', 'description', 'application_process', 'organizations',
# 'id', 'y-org status', 'organization_ids', 'taxonomy_ids', 'email', 'phones', 'fees',
# 'phone_ids', 'locations', 'address', 'location_ids', 'alternate_name', 'contacts',
# 'status', 'schedule', 'schedule_ids', 'interpretation_services', 'programs',
# 'accreditations', 'wait_time', 'licenses']