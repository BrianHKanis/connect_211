from build_tables.tables import build_dict, reduce_dict, reduce_dict_multiple_values
from build_tables.tables import airtable_key, base_id, table_id_dict, headers

hsds_columns = ["id", "organization_id", "program_id", "name", "alternate_name",
            "description", "url", "email", "status", "interpretation_services",
            "application_process", "fees_description", "wait_time", "fees",
            "accreditations", "eligibility_description", "minimum_age", "maximum_age",
            "assured_date", "assurer_email", "licenses", "alert", "last_modified",
            "phones", "schedules", "service_areas", "service_at_locations", "languages",
            "organization", "funding", "cost_options", "program", "required_documents",
            "contacts", "attributes", "metadata"]

required = ['id', 'name', 'status']

def delete_or_rename_columns(core_dict):
    for record in core_dict:
        if 'interpretation_services' in record.keys():
            record['languages'] = record['interpretation_services']
        if 'schedule' in record.keys():
            record['schedules'] = record['schedule']
        if 'location_ids' in record.keys():
            record['service_areas'] = record['location_ids']
        if 'taxonomy_ids' in record.keys():
            record['service_at_locations'] = record['taxonomy_ids']
    for record in core_dict:
        for k, v in list(record.items()):
            if k not in hsds_columns:
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

def get_service_at_location(core_dict, reduced_tax_dict):
    for record in core_dict:
        if 'service_at_locations' in record.keys():
            tax_ids = record['service_at_locations']
            terms = [reduced_tax_dict[tax_id] for tax_id in tax_ids]
            record['service_at_locations'] = terms
    return core_dict

def complete_table():
    service_records = build_dict('services')
    services_hsds = delete_or_rename_columns(service_records)
    services_hsds_all = add_required_if_missing(services_hsds)
    schedule_records = build_dict('schedule')
    address_records = build_dict('physical_addresses')
    taxonomy_records = build_dict('taxonomy_terms')
    
    reduced_schedules = reduce_dict_multiple_values(schedule_records, 'id', ['opens_at', 'closes_at', 'byday', 'description'])
    reduced_addresses = reduce_dict(address_records, 'location_ids', 'city')
    reduced_taxonomies = reduce_dict(taxonomy_records, 'id', 'term')

    services_with_service_at_location = get_service_at_location(services_hsds_all, reduced_taxonomies)
    services_with_schedules = get_schedules(services_with_service_at_location, reduced_schedules)
    services_with_addresses = get_service_area(services_with_schedules, reduced_addresses)
    return services_with_addresses


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