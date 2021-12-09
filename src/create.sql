-- Create Tables for Crime Database

\! rm -f output_create.txt
tee output_create.txt

DROP TABLE IF EXISTS Crime;
DROP TABLE IF EXISTS Complaint;
DROP TABLE IF EXISTS Search;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Code;
DROP TABLE IF EXISTS Incident;
DROP TABLE IF EXISTS Location;

CREATE TABLE Incident (
    incident_id INT NOT NULL AUTO_INCREMENT,
    location_id INT,
    occurence_date DATE,
    type VARCHAR(128),
    PRIMARY KEY(incident_id)
);

CREATE TABLE Location (
    location_id INT NOT NULL AUTO_INCREMENT,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(64),
    lsoa_code CHAR(9),
    borough VARCHAR(64),
    city VARCHAR(64),
    country VARCHAR(32),
    PRIMARY KEY(location_id)
);

CREATE TABLE Crime (
    crime_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    code INT,
    organization INT,
    victim_id INT,
    description VARCHAR(256),
    PRIMARY KEY(crime_id)
);

CREATE TABLE Complaint (
    complaint_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    code INT,
    organization INT,
    report_date DATE,
    description VARCHAR(256),
    PRIMARY KEY(complaint_id)
);

CREATE TABLE Search (
    search_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    suspect_id INT,
    legislation VARCHAR(128),
    object VARCHAR(64),
    outcome VARCHAR(128),
    object_caused_outcome BOOL,
    clothing_removal BOOL,
    PRIMARY KEY(search_id)
);

CREATE TABLE Person (
    person_id INT NOT NULL AUTO_INCREMENT,
    age_range VARCHAR(16),
    gender VARCHAR(16),
    ethnicity VARCHAR(16),
    PRIMARY KEY(person_id)
);

CREATE TABLE Code (
    code DECIMAL(3) NOT NULL,
    organization VARCHAR(16) NOT NULL,
    category VARCHAR(64),
    description VARCHAR(256),
    PRIMARY KEY(code, organization)
);

notee