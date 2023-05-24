from build_tables.tables import build_dict, reduce_dict, reduce_dict_multiple_values
from build_tables.tables import airtable_key, base_id, table_id_dict, headers
from build_tables.hsds_columns import locations_columns, address_columns, schedule_columns

required = ['id', 'location_type']

def delete_or_rename_columns(core_dict):
    # Renames
    for record in core_dict:
        if 'schedule' in record.keys():
            record['schedules'] = record['schedule']
    # Deletes
    for record in core_dict:
        for k, v in list(record.items()):
            if k not in locations_columns:
                del record[k]
    return core_dict

def add_required_if_missing(core_dict):
    for record in core_dict:
        if 'location_type' not in record.keys():
            record['location_type'] = ''
        if 'id' not in record.keys():
            record['id'] = ''
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
            if len(schedule_ids) > 1:
                schedules = [reduced_schedule_dict[id] for id in schedule_ids]
                record['schedules'] = schedules
            else:
                schedule = reduced_schedule_dict[schedule_ids[0]]
                record['schedules'] = schedule    
    return core_dict

def get_phones(core_dict, reduced_phone_dict):
    for record in core_dict:
        if 'phones' in record.keys():
            phone_ids = record['phones']
            phone_numbers = [reduced_phone_dict[phone_id] for phone_id in phone_ids]
            record['phones'] = phone_numbers
    return core_dict

# def get_contacts(core_dict, reduced_contact_dict)
#     pass

def complete_table():
    location_records = build_dict('locations')
    address_records = build_dict('physical_addresses')
    schedules_records = build_dict('schedule')
    phone_records = build_dict('phones')
    # contact_records = build_dict('contacts')

    locations_hsds = delete_or_rename_columns(location_records)

    # reduced_contacts = reduce_dict_multiple_values()


    reduced_addresses = reduce_dict_multiple_values(address_records, 'id', address_columns)
    reduced_schedules = reduce_dict_multiple_values(schedules_records, 'id', schedule_columns)
    reduced_phones = reduce_dict(phone_records, 'id', 'number')


    locations_with_addresses = get_addresses(locations_hsds, reduced_addresses)
    locations_with_schedules = get_schedules(locations_with_addresses, reduced_schedules)
    locations_with_phones = get_phones(locations_with_schedules, reduced_phones)
    locations_hsds_complete = add_required_if_missing(locations_with_phones)
    return locations_hsds_complete

# HSDS
# "id": ▹{...}, #
# "location_type": ▹{...}, !
# "url": ▹{...}, Service url? !
# "organization_id": ▹{...}, #
# "name": ▹{...}, #
# "alternate_name": ▹{...}, #
# "description": ▹{...}, #
# "transportation": ▹{...}, empty #
# "latitude": ▹{...}, empty #
# "longitude": ▹{...}, empty #
# "external_identifier": ▹{...}, !
# "external_identifier_type": ▹{...}, !
# "languages": ▹{...}, service interpretation services? !
# "addresses": ▹{...}, #
# "contacts": ▹{...}, !
# "accessibility": ▹{...}, !
# "phones": ▹{...}, #
# "schedules": ▹{...}, #
# "attributes": ▹{...}, !
# "metadata": ▹{...} !

# Airtable
# ['services', 'name', 'organization', 'address', 'id', 'organization_ids',
# 'service_ids', 'geocode', 'phones', 'schedule', 'description', 'alternate_name']