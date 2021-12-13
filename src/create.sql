-- ////////////////////////////////////////////////////////////////////////
-- Create tables for crime database
-- ////////////////////////////////////////////////////////////////////////


-- ////////////////////////////////////////////////////////////////////////
-- Log output to file
-- ////////////////////////////////////////////////////////////////////////

\! rm -f output_create.txt
tee output_create.txt

-- ////////////////////////////////////////////////////////////////////////
-- Drop all tables
-- ////////////////////////////////////////////////////////////////////////

DROP TABLE IF EXISTS Crime;
DROP TABLE IF EXISTS Complaint;
DROP TABLE IF EXISTS Search;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Code;
DROP TABLE IF EXISTS Incident;
DROP TABLE IF EXISTS Location;

DROP TABLE IF EXISTS LondonStopAndSearch;
DROP TABLE IF EXISTS LondonOutcomes;
DROP TABLE IF EXISTS LondonStreet;
DROP TABLE IF EXISTS NYPDComplaint;

-- ////////////////////////////////////////////////////////////////////////
-- Create tables
-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE Incident (
    incident_id INT NOT NULL AUTO_INCREMENT,
    location_id INT,
    occurrence_date DATE,
    type VARCHAR(128),
    PRIMARY KEY(incident_id)
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE Location (
    location_id INT NOT NULL AUTO_INCREMENT,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    lsoa_code CHAR(9),
    borough VARCHAR(64),
    city VARCHAR(64),
    state VARCHAR(64),
    country VARCHAR(64),
    PRIMARY KEY(location_id)
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE Crime (
    crime_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    code VARCHAR(4),
    organization VARCHAR(16),
    victim_id INT,
    description VARCHAR(256),
    PRIMARY KEY(crime_id)
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE Complaint (
    complaint_id INT NOT NULL AUTO_INCREMENT,
    incident_id INT,
    code VARCHAR(4),
    organization VARCHAR(16),
    reported_date DATE,
    description VARCHAR(256),
    PRIMARY KEY(complaint_id)
);

-- ////////////////////////////////////////////////////////////////////////

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

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE Person (
    person_id INT NOT NULL AUTO_INCREMENT,
    age_range VARCHAR(16),
    gender VARCHAR(16),
    ethnicity VARCHAR(64),
    PRIMARY KEY(person_id)
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE Code (
    code VARCHAR(4) NOT NULL,
    organization VARCHAR(16) NOT NULL,
    category VARCHAR(256),
    description VARCHAR(256),
    PRIMARY KEY(code, organization)
);

-- ////////////////////////////////////////////////////////////////////////
-- Create temporary tables
-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE LondonStopAndSearch (
    type VARCHAR(128),
    occurrence_date DATE,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    gender VARCHAR(16),
    age_range VARCHAR(16),
    ethnicity VARCHAR(64),
    legislation VARCHAR(256),
    object VARCHAR(256),
    outcome VARCHAR(256),
    object_caused_outcome BOOL,
    clothing_removal BOOL
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE LondonOutcomes (
    occurrence_date DATE,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    lsoa_code CHAR(9),
    description VARCHAR(256)
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE LondonStreet (
    occurrence_date DATE,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    lsoa_code CHAR(9),
    type VARCHAR(128),
    description VARCHAR(256)
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE NYPDComplaints (
    occurrence_date DATE,
    reported_date DATE,
    code VARCHAR(4),
    organization VARCHAR(16),
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    borough VARCHAR(64),
    type VARCHAR(128),
    description VARCHAR(256)
);

-- ////////////////////////////////////////////////////////////////////////

CREATE TABLE ChicagoCrimes (
    occurrence_date DATE,
    code VARCHAR(4),
    organization VARCHAR(16),
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    borough VARCHAR(64)
);

-- ////////////////////////////////////////////////////////////////////////

notee