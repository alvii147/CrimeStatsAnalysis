CREATE TABLE LondonStopAndSearch (
    type VARCHAR(128),
    occurrence_date DATE,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    age_range VARCHAR(16),
    gender VARCHAR(16),
    ethnicity VARCHAR(64),
    legislation VARCHAR(256),
    object VARCHAR(256),
    outcome VARCHAR(256),
    object_caused_outcome BOOL,
    clothing_removal BOOL
);

CREATE TABLE LondonOutcomes (
    occurrence_date DATE,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    borough VARCHAR(64),
    description VARCHAR(256)
);

CREATE TABLE LondonStreet (
    occurrence_date DATE,
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    borough VARCHAR(64),
    type VARCHAR(128),
    description VARCHAR(256)
);

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

CREATE TABLE ChicagoCrimes (
    occurrence_date DATE,
    code VARCHAR(4),
    organization VARCHAR(16),
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    precinct VARCHAR(128),
    borough VARCHAR(64)
);

CREATE TABLE LACrimes (
    occurrence_date DATE,
    code VARCHAR(4),
    organization VARCHAR(16),
    latitude DECIMAL(11, 8),
    longitude DECIMAL(11, 8),
    age_range VARCHAR(16),
    gender VARCHAR(16),
    ethnicity VARCHAR(64),
    borough VARCHAR(64),
    precinct VARCHAR(128)
);
