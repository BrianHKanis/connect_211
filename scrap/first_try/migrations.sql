DROP TABLE IF EXISTS organizations;


CREATE TABLE organizations (
    name VARCHAR,
    alternate_name VARCHAR,
    x_status VARCHAR,
    x_verification VARCHAR,
    Service_Area VARCHAR,
    phones VARCHAR,
    url VARCHAR,
    description VARCHAR,
    services VARCHAR,
    email VARCHAR,
    locations VARCHAR,
    x_website_rating VARCHAR,
    x_status_last_modified VARCHAR,
    id VARCHAR
);

\copy organizations (name, alternate_name, x_status, x_verification, Service_Area, phones, url, description, services, email, locations, x_website_rating, x_status_last_modified, id) FROM 'organizations/organizations-Grid view.csv' DELIMITER ',' CSV HEADER;