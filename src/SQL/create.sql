CREATE TABLE Incident (
    incident_id INT NOT NULL AUTO_INCREMENT,
    location_id INT,
    occurrence_date DATE,
    police_department VARCHAR(256),
    type VARCHAR(128),
    PRIMARY KEY(incident_id)
);

CREATE TABLE Location (
    location_id INT NOT NULL AUTO_INCREMENT,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    premises VARCHAR(128),
    area VARCHAR(256),
    precinct DECIMAL(4),
    ward DECIMAL(3),
    borough VARCHAR(64),
    city VARCHAR(64),
    state VARCHAR(64),
    country VARCHAR(64),
    PRIMARY KEY(location_id)
);

CREATE TABLE Crime (
    crime_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    code VARCHAR(4),
    organization VARCHAR(16),
    victim_id INT,
    weapon VARCHAR(256),
    description VARCHAR(256),
    PRIMARY KEY(crime_id)
);

CREATE TABLE Complaint (
    complaint_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    code VARCHAR(4),
    organization VARCHAR(16),
    reported_date DATE,
    description VARCHAR(256),
    PRIMARY KEY(complaint_id)
);

CREATE TABLE Search (
    search_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    suspect_id INT,
    legislation VARCHAR(256),
    object VARCHAR(256),
    outcome VARCHAR(256),
    object_caused_outcome BOOL,
    clothing_removal BOOL,
    PRIMARY KEY(search_id)
);

CREATE TABLE Person (
    person_id INT NOT NULL AUTO_INCREMENT,
    age_range VARCHAR(16),
    gender VARCHAR(16),
    ethnicity VARCHAR(64),
    PRIMARY KEY(person_id)
);

CREATE TABLE Code (
    code VARCHAR(4) NOT NULL,
    organization VARCHAR(16) NOT NULL,
    category VARCHAR(256),
    description VARCHAR(256),
    PRIMARY KEY(code, organization)
);
