from build_tables.tables import build_dict, reduce_dict, reduce_dict_multiple_values
from build_tables.tables import airtable_key, base_id, table_id_dict, headers
from build_tables.hsds_columns import organizations_columns, phones_columns, programs_columns, contact_columns, locations_columns

required= ['id', 'name', 'description']


def delete_or_rename_columns(core_dict: list) -> list:
    # Renames
    for record in core_dict:
        if 'url' in record.keys():
            record['website'] = record['url']
        if 'services' in record.keys():
            record['contacts'] = record['services']
    # Deletes
    for record in core_dict:
        for k, v in list(record.items()):
            if k not in organizations_columns:
                del record[k]
    return core_dict

def add_required_if_missing(core_dict):
    for record in core_dict:
        if 'id' not in record.keys():
            record['id'] = ''
        if 'name' not in record.keys():
            record['name'] = ''
        if 'description' not in record.keys():
            record['description'] = ''
    return core_dict

def rename_sub_columns(core_dict):
    for record in core_dict:
        if 'programs' in record.keys():
            program_records = record['programs']
            for program in program_records:
                if 'term' in program.keys():
                    program['name'] = program['term']
                    del program['term']
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

def get_locations(core_dict, reduced_location_dict):
    for record in core_dict:
        if 'locations' in record.keys():
            location_ids = record['locations']
            locations = [reduced_location_dict[id] for id in location_ids]
            record['locations'] = locations
    return core_dict

def get_programs(core_dict, reduced_services, reduced_taxonomy_terms):
    for record in core_dict:
        if 'id' in record.keys():
            org_id = record['id']
            tax_ids = reduced_services[org_id]
            tax_terms = [reduced_taxonomy_terms[tax_id] for tax_id in tax_ids]
            record['programs'] = tax_terms
    return core_dict

def get_contacts(core_dict, reduced_contacts):
    #Link through services with id before get_services is called
    for record in core_dict:
        if 'contacts' in record.keys():
            service_ids = record['contacts']
            contacts = []
            for id in service_ids:
                if id in reduced_contacts.keys():
                    contacts.append(reduced_contacts[id])
            if len(contacts) > 0:                    
                record['contacts'] = contacts
            else:
                del record['contacts']
    return core_dict

def complete_table(complete_locations_table):
    org_records = build_dict('organizations')
    orgs_hsds = delete_or_rename_columns(org_records)

    phone_records = build_dict('phones')
    location_records = complete_locations_table
    service_records = build_dict('services')
    taxonomy_records = build_dict('taxonomy_terms')
    contact_records = build_dict('contacts')

    reduced_phones = reduce_dict_multiple_values(phone_records, 'id', phones_columns)
    reduced_locations = reduce_dict_multiple_values(location_records, 'id', locations_columns)
    reduced_services = reduce_dict(service_records, 'organization_ids', 'taxonomy_ids')
    reduced_taxonomy_terms = reduce_dict_multiple_values(taxonomy_records, 'id', programs_columns)

    contacts_with_phones = get_phones(contact_records, reduced_phones)
    reduced_contacts = reduce_dict_multiple_values(contacts_with_phones, 'services', contact_columns)

    orgs_with_phone = get_phones(orgs_hsds, reduced_phones)
    orgs_with_locations = get_locations(orgs_with_phone, reduced_locations)
    orgs_with_programs = get_programs(orgs_with_locations, reduced_services, reduced_taxonomy_terms)
    orgs_with_contacts = get_contacts(orgs_with_programs, reduced_contacts)
    orgs_with_sub_columns = rename_sub_columns(orgs_with_contacts)
    return orgs_with_sub_columns


# HSDS 3.0
# "id": ▹{...}, #
# "name": ▹{...}, #
# "alternate_name": ▹{...}, #
# "description": ▹{...}, #
# "email": ▹{...}, #
# "website": ▹{...}, # --> 'url'
# "tax_status": ▹{...}, # Empty for all but one record
# "tax_id": ▹{...}, Included but is empty for every record.
# "year_incorporated": ▹{...}, Included but empty
# "legal_status": ▹{...}, Included but empty
# "logo": ▹{...}, "x-logo" Included but empty
# "uri": ▹{...}, uri is same as url and website? ! --- Nulls
# "parent_organization_id": ▹{...}, Not included !
# "funding": ▹{...}, Not included !
# "contacts": ▹{...}, Not included Is different from phone and email? !
# "phones": ▹{...}, Included #
# "locations": ▹{...}, # Included #
# "programs": ▹{...}, Not included. Same as services? !     --- Nulls
# "organization_identifiers": ▹{...}, Not included !
# "attributes": ▹{...}, Not included. Service description? !
# "metadata": ▹{...} Not included. Record of changes. !

# Airtable
# ['phones', 'locations', 'x-status', 'url', 'x-update', 'name',
# 'x-verification', 'description', 'services', 'x-website rating',
# 'Service Area', 'x-assigned to', 'x-status_last_modified',
# 'y-Number of Services', 'id', 'email', 'alternate_name', 'tax_status']

# for org in organizations_dicts:
#   if 'email' in org.keys():
#             print(org['email'])