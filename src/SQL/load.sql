LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-stop-and-search.csv'
INTO TABLE LondonStopAndSearch
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 302524 LINES
(type, @_occurrence_date, @_dummy, @_dummy, @_latitude, @_longitude, @_gender, @_age_range, @_dummy, @_ethnicity, @_legislation, @_object, @_outcome, @_object_caused_outcome, @_clothing_removal)
SET
    gender = NULLIF(@_gender, ''),
    age_range = NULLIF(@_age_range, ''),
    ethnicity = NULLIF(@_ethnicity, ''),
    legislation = NULLIF(@_legislation, ''),
    object = NULLIF(@_object, ''),
    outcome = NULLIF(@_outcome, ''),
    occurrence_date = CAST(@_occurrence_date AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, ''),
    object_caused_outcome = CAST(@_object_caused_outcome = 'True' AS UNSIGNED),
    clothing_removal = CAST(@_clothing_removal = 'True' AS UNSIGNED);

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-outcomes.csv'
INTO TABLE LondonOutcomes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 1946951 LINES
(@_dummy, @_occurrence_date, @_dummy, @_dummy, @_longitude, @_latitude, @_dummy, @_dummy, @_borough, @_description)
SET
    description = NULLIF(@_description, ''),
    occurrence_date = CAST(CONCAT(@_occurrence_date, '-01') AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, ''),
    borough = NULLIF(@_borough, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-street.csv'
INTO TABLE LondonStreet
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 2946380 LINES
(@_dummy, @_occurrence_date, @_dummy, @_longitude, @_latitude, @_dummy, @_dummy, @_borough, @_type, @_description, @_dummy)
SET
    type = NULLIF(@_type, ''),
    description = NULLIF(@_description, ''),
    occurrence_date = CAST(CONCAT(@_occurrence_date, '-01') AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, ''),
    borough = NULLIF(@_borough, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/NYPD_Complaint_Data_Historic.csv'
INTO TABLE NYPDComplaints
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\r\n'
IGNORE 1048476 LINES
(@_dummy, @_occurrence_date, @_dummy, @_dummy, @_dummy, @_reported_date, @_code, @_dummy, @_dummy, @_description, @_dummy, @_type, @_dummy, @_borough, @_precinct, @_premises_preposition, @_premises_description, @_dummy, @_dummy, @_dummy, @_dummy, @_latitude, @_longitude, @_dummy)
SET
    code = NULLIF(@_code, ''),
    description = NULLIF(@_description, ''),
    type = NULLIF(@_type, ''),
    premises = TRIM(CONCAT(@_premises_preposition, ' ', @_premises_description)),
    precinct = NULLIF(@_precinct, ''),
    borough = NULLIF(@_borough, ''),
    occurrence_date = CAST(STR_TO_DATE(@_occurrence_date,'%d/%m/%Y') AS DATE),
    reported_date = CAST(STR_TO_DATE(@_reported_date,'%d/%m/%Y') AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2001_to_2004.csv'
INTO TABLE ChicagoCrimes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 1923423 LINES
(@_dummy, @_dummy, @_dummy, @_occurrence_date, @_dummy, @_code, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_borough, @_precinct, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_latitude, @_longitude, @_dummy)
SET
    borough = NULLIF(@_borough, ''),
    precinct = NULLIF(@_precinct, ''),
    occurrence_date = CAST(STR_TO_DATE(@_occurrence_date, '%m/%d/%Y %h:%i:%s %p') AS DATE),
    code = TRIM(LEADING '0' FROM @_code),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2005_to_2007.csv'
INTO TABLE ChicagoCrimes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 1872245 LINES
(@_dummy, @_dummy, @_dummy, @_occurrence_date, @_dummy, @_code, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_borough, @_precinct, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_latitude, @_longitude, @_dummy)
SET
    borough = NULLIF(@_borough, ''),
    precinct = NULLIF(@_precinct, ''),
    occurrence_date = CAST(STR_TO_DATE(@_occurrence_date, '%m/%d/%Y %h:%i:%s %p') AS DATE),
    code = TRIM(LEADING '0' FROM @_code),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2008_to_2011.csv'
INTO TABLE ChicagoCrimes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 2688611 LINES
(@_dummy, @_dummy, @_dummy, @_occurrence_date, @_dummy, @_code, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_borough, @_precinct, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_latitude, @_longitude, @_dummy)
SET
    borough = NULLIF(@_borough, ''),
    precinct = NULLIF(@_precinct, ''),
    occurrence_date = CAST(STR_TO_DATE(@_occurrence_date, '%m/%d/%Y %h:%i:%s %p') AS DATE),
    code = TRIM(LEADING '0' FROM @_code),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2012_to_2017.csv'
INTO TABLE ChicagoCrimes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 1456615 LINES
(@_dummy, @_dummy, @_dummy, @_occurrence_date, @_dummy, @_code, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_borough, @_precinct, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_latitude, @_longitude, @_dummy)
SET
    borough = NULLIF(@_borough, ''),
    precinct = NULLIF(@_precinct, ''),
    occurrence_date = CAST(STR_TO_DATE(@_occurrence_date, '%m/%d/%Y %h:%i:%s %p') AS DATE),
    code = TRIM(LEADING '0' FROM @_code),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/Crime_Data_from_2010_to_2019.csv'
INTO TABLE LACrimes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 2116140 LINES
(@_dummy, @_dummy, @_occurrence_date, @_dummy, @_precinct, @_borough, @_dummy, @_dummy, @_code, @_dummy, @_dummy, @_age_range, @_gender, @_ethnicity, @_dummy, @_dummy, @_dummy, @_weapon, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_premises, @_dummy, @_latitude, @_longitude)
SET
    precinct = NULLIF(@_precinct, ''),
    code = NULLIF(@_code, ''),
    age_range = NULLIF(@_age_range, ''),
    occurrence_date = CAST(STR_TO_DATE(@_occurrence_date, '%m/%d/%Y %h:%i:%s %p') AS DATE),
    gender =
        CASE
            WHEN UPPER(@_gender) = 'M' THEN 'Male'
            WHEN UPPER(@_gender) = 'F' THEN 'Female'
            ELSE 'Other'
        END,
    ethnicity =
        CASE
            WHEN UPPER(@_ethnicity) = 'A' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'B' THEN 'Black'
            WHEN UPPER(@_ethnicity) = 'C' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'D' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'F' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'H' THEN 'Hispanic'
            WHEN UPPER(@_ethnicity) = 'J' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'K' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'V' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'W' THEN 'White'
            WHEN UPPER(@_ethnicity) = 'Z' THEN 'Asian'
            ELSE 'Other'
        END,
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, ''),
    premises = REGEXP_REPLACE(@_premises, '[[:space:]]+', ' '),
    borough = NULLIF(@_borough, ''),
    weapon = NULLIF(@_weapon, '');

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/Crime_Data_from_2020_to_Present.csv'
INTO TABLE LACrimes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 182536 LINES
(@_dummy, @_dummy, @_occurrence_date, @_dummy, @_precinct, @_borough, @_dummy, @_dummy, @_code, @_dummy, @_dummy, @_age_range, @_gender, @_ethnicity, @_dummy, @_dummy, @_dummy, weapon, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_premises, @_dummy, @_latitude, @_longitude)
SET
    precinct = NULLIF(@_precinct, ''),
    code = NULLIF(@_code, ''),
    age_range = NULLIF(@_age_range, ''),
    occurrence_date = CAST(STR_TO_DATE(@_occurrence_date, '%m/%d/%Y %h:%i:%s %p') AS DATE),
    gender =
        CASE
            WHEN UPPER(@_gender) = 'M' THEN 'Male'
            WHEN UPPER(@_gender) = 'F' THEN 'Female'
            ELSE 'Other'
        END,
    ethnicity =
        CASE
            WHEN UPPER(@_ethnicity) = 'A' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'B' THEN 'Black'
            WHEN UPPER(@_ethnicity) = 'C' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'D' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'F' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'H' THEN 'Hispanic'
            WHEN UPPER(@_ethnicity) = 'J' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'K' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'V' THEN 'Asian'
            WHEN UPPER(@_ethnicity) = 'W' THEN 'White'
            WHEN UPPER(@_ethnicity) = 'Z' THEN 'Asian'
            ELSE 'Other'
        END,
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, ''),
    premises = REGEXP_REPLACE(@_premises, '[[:space:]]+', ' '),
    borough = NULLIF(@_borough, ''),
    weapon = NULLIF(@_weapon, '');
