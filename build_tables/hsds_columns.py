organizations_columns = ['id', 'name', 'alternate_name', 'description', 'email', 'website',
                         'tax_status', 'tax_id', 'year_incorporated', 'legal_status', 'logo',
                         'uri', 'parent_organization', 'funding', 'contacts', 'phones',
                         'locations', 'programs', 'organization_identifiers', 'attributes'
                         'metadata']

locations_columns = ["id", "location_type", "url", "organization_id", "name",
                "alternate_name", "description", "transportation", "latitude",
                "longitude", "external_identifier", "external_identifier_type",
                "languages", "addresses", "contacts", "accessibility", "phones",
                "schedules", "attributes", "metadata"]

services_columns = ["id", "organization_id", "program_id", "name", "alternate_name",
            "description", "url", "email", "status", "interpretation_services",
            "application_process", "fees_description", "wait_time", "fees",
            "accreditations", "eligibility_description", "minimum_age", "maximum_age",
            "assured_date", "assurer_email", "licenses", "alert", "last_modified",
            "phones", "schedules", "service_areas", "service_at_locations", "languages",
            "organization", "funding", "cost_options", "program", "required_documents",
            "contacts", "attributes", "metadata"]

services_at_location_columns = ['id', 'service_id', 'location_id', 'description',
                                'contacts', 'phones', 'schedules', 'location',
                                'attributes', 'metadata']


schedule_columns = ['id', 'valid_from', 'valid_to', 'dtstart', 'timezone', 'until',
                'count', 'wkst', 'freq', 'interval' 'byday', 'byweekno', 'bymonthday',
                'byyearday', 'description', 'opens_at', 'closes_at', 'schedule_link',
                'attending_type' 'notes']

phones_columns = ['id', 'number', 'extension', 'type', 'description', 'languages']

address_columns = ['id', 'attention', 'address_1', 'address_2', 'city', 'region',
                   'state_province', 'postal_code', 'country', 'address_type']