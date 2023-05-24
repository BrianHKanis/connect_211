from build_tables.tables import build_dict, reduce_dict, reduce_dict_multiple_values
from build_tables.tables import airtable_key, base_id, table_id_dict, headers
from build_tables.hsds_columns import services_columns, schedule_columns, phones_columns, contact_columns, services_at_location_columns, organizations_columns

required = ['id', 'name', 'status']

def delete_or_rename_columns(core_dict):
    for record in core_dict:
        if 'interpretation_services' in record.keys():
            record['languages'] = record['interpretation_services']
        if 'schedule' in record.keys():
            record['schedules'] = record['schedule']
        if 'location_ids' in record.keys():
            record['service_areas'] = record['location_ids']
        if 'organization_ids' in record.keys():
            record['organization'] = record['organization_ids']
        # if 'taxonomy_ids' in record.keys():
        #     record['service_at_locations'] = record['taxonomy_ids']
    for record in core_dict:
        for k, v in list(record.items()):
            if k not in services_columns:
                del record[k]
    return core_dict

def add_required_if_missing(core_dict):
    for record in core_dict:
        if 'id' not in record.keys():
            record['id'] = ''
        if 'name' not in record.keys():
            record['name'] = ''
        if 'status' not in record.keys():
            record['status'] = ''
    return core_dict

def get_schedules(core_dict, reduced_schedule_dict):
    for record in core_dict:
        if 'schedules' in record.keys():
            schedule_ids = record['schedules']
            if len(schedule_ids) > 1:
                schedules = [reduced_schedule_dict[schedule_id] for schedule_id in schedule_ids]
            else:
                schedules = reduced_schedule_dict[schedule_ids[0]]
            record['schedules'] = schedules
    return core_dict

def get_service_area(core_dict, reduced_addresses_dict):
    for record in core_dict:
        if 'service_areas' in record.keys():
            location_ids = record['service_areas']
            city_names = [reduced_addresses_dict[loc_id] for loc_id in location_ids if loc_id in reduced_addresses_dict.keys()]
            record['service_areas'] = city_names
    return core_dict

# def get_service_at_location(core_dict, reduced_tax_dict):
#     for record in core_dict:
#         if 'service_at_locations' in record.keys():
#             tax_ids = record['service_at_locations']
#             terms = [reduced_tax_dict[tax_id] for tax_id in tax_ids]
#             record['service_at_locations'] = terms
#     return core_dict

# Update servie_at_location with completed dictionary
def get_service_at_location(core_dict, reduced_service_at_location_dict):
    for record in core_dict:
        if 'id' in record.keys():
            service_id = record['id']
            service_at_location = reduced_service_at_location_dict[service_id]
            record['service_at_locations'] = service_at_location
    return core_dict

def get_phones(core_dict, reduced_phone_dict):
    for record in core_dict:
        phone_numbers = []
        if 'phones' in record.keys():
            phone_ids = record['phones']
            for phone_id in phone_ids:
                phone_numbers.append(reduced_phone_dict[phone_id])
            record['phones'] = phone_numbers
    return core_dict

def get_contacts(core_dict, reduced_contact_dict):
    for record in core_dict:
        if 'contacts' in record.keys():
            contact_ids = record['contacts']
            contacts = [reduced_contact_dict[con_id] for con_id in contact_ids]
            record['contacts'] = contacts
    return core_dict

def get_organizations(core_dict, reduced_organizations_dict):
    for record in core_dict:
        if 'organization' in record.keys():
            organization_ids = record['organization']
            organization = [reduced_organizations_dict[org_id] for org_id in organization_ids]
            record['organization'] = organization
    return core_dict

def get_program(core_dict, reduced_programs_dict):
    pass

def complete_table(organization_table, service_at_location_table): ##
    service_records = build_dict('services')
    services_hsds = delete_or_rename_columns(service_records)
    services_hsds_all = add_required_if_missing(services_hsds)
    schedule_records = build_dict('schedule')
    address_records = build_dict('physical_addresses')
    # taxonomy_records = build_dict('taxonomy_terms')
    phone_records = build_dict('phones')
    contact_records = build_dict('contacts')
    service_at_location_records = service_at_location_table ##
    organization_records = organization_table

    reduced_schedules = reduce_dict_multiple_values(schedule_records, 'id', schedule_columns)
    reduced_addresses = reduce_dict_multiple_values(address_records, 'location_ids', ['city', 'state'])
    # reduced_taxonomies = reduce_dict(taxonomy_records, 'id', 'term')
    reduced_phones = reduce_dict_multiple_values(phone_records, 'id', phones_columns)
    contacts_with_phones = get_phones(contact_records, reduced_phones)
    reduced_contacts = reduce_dict_multiple_values(contacts_with_phones, 'id', contact_columns)
    reduced_service_at_locations = reduce_dict_multiple_values(service_at_location_records, 'id', services_at_location_columns)
    reduced_organizations = reduce_dict_multiple_values(organization_records, 'id', organizations_columns)

    # services_with_service_at_location = get_service_at_location(services_hsds_all, reduced_taxonomies)
    services_with_service_at_location = get_service_at_location(services_hsds_all, reduced_service_at_locations)
    services_with_schedules = get_schedules(services_with_service_at_location, reduced_schedules)
    services_with_addresses = get_service_area(services_with_schedules, reduced_addresses)
    services_with_phones = get_phones(services_with_addresses, reduced_phones)
    services_with_contacts = get_contacts(services_with_phones, reduced_contacts)
    services_with_organizations = get_organizations(services_with_contacts, reduced_organizations)

    return services_with_organizations


# HSDS 3.0
# "id": ▹{...}, #
# "organization_id": ▹{...}, #
# "program_id": ▹{...}, # id
# "name": ▹{...}, #
# "alternate_name": ▹{...}, #
# "description": ▹{...}, #
# "url": ▹{...}, #
# "email": ▹{...}, #
# "status": ▹{...}, #
# "interpretation_services": ▹{...}, #
# "application_process": ▹{...}, #
# "fees_description": ▹{...}, # fees
# "wait_time": ▹{...}, #
# "fees": ▹{...}, Only description. Some have values within text !
# "accreditations": ▹{...}, #
# "eligibility_description": ▹{...}, Not included !
# "minimum_age": ▹{...}, !
# "maximum_age": ▹{...}, !
# "assured_date": ▹{...}, !
# "assurer_email": ▹{...}, ?!
# "licenses": ▹{...}, #
# "alert": ▹{...}, !
# "last_modified": ▹{...}, Created time? !
# "phones": ▹{...}, #
# "schedules": ▹{...}, Included as ID #
# "service_areas": ▹{...}, City from address? !
# "service_at_locations": ▹{...}, Service name or description? !
# "languages": ▹{...}, interpretation_services #
# "organization": ▹{...}, org.name where services.org_id matches #
# "funding": ▹{...}, !
# "cost_options": ▹{...}, !
# "program": ▹{...}, Description? !
# "required_documents": ▹{...}, !
# "contacts": ▹{...}, ! through services
# "attributes": ▹{...}, Description? ! 
# "metadata": ▹{...} Record of changes ! Omit

# Airtable
# ['name', 'url', 'taxonomy', 'description', 'application_process', 'organizations',
# 'id', 'y-org status', 'organization_ids', 'taxonomy_ids', 'email', 'phones', 'fees',
# 'phone_ids', 'locations', 'address', 'location_ids', 'alternate_name', 'contacts',
# 'status', 'schedule', 'schedule_ids', 'interpretation_services', 'programs',
# 'accreditations', 'wait_time', 'licenses']