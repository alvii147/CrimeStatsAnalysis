-- ////////////////////////////////////////////////////////////////////////
-- Load tables with data for crime database
-- ////////////////////////////////////////////////////////////////////////


-- ////////////////////////////////////////////////////////////////////////
-- Log output to file
-- ////////////////////////////////////////////////////////////////////////

\! rm -f output_load.txt
tee output_load.txt

-- ////////////////////////////////////////////////////////////////////////
-- Load temporary tables with data
-- ////////////////////////////////////////////////////////////////////////

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-stop-and-search.csv'
INTO TABLE LondonStopAndSearch
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 302524 LINES
(type, @_occurrence_date, @_dummy, @_dummy, @_latitude, @_longitude, gender, age_range, @_dummy, ethnicity, legislation, object, outcome, @_object_caused_outcome, @_clothing_removal)
SET
    occurrence_date = CAST(@_occurrence_date AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, ''),
    object_caused_outcome = CAST(@_object_caused_outcome = 'True' AS UNSIGNED),
    clothing_removal = CAST(@_clothing_removal = 'True' AS UNSIGNED);

-- ////////////////////////////////////////////////////////////////////////

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-outcomes.csv'
INTO TABLE LondonOutcomes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 1946951 LINES
(@_dummy, @_occurrence_date, precinct, @_dummy, @_longitude, @_latitude, @_dummy, lsoa_code, @_dummy, description)
SET
    occurrence_date = CAST(CONCAT(@_occurrence_date, '-01') AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

-- ////////////////////////////////////////////////////////////////////////

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-street.csv'
INTO TABLE LondonStreet
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 2946580 LINES
(@_dummy, @_occurrence_date, precinct, @_dummy, @_longitude, @_latitude, @_dummy, lsoa_code, @_dummy, type, description, @_dummy)
SET
    occurrence_date = CAST(CONCAT(@_occurrence_date, '-01') AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

-- ////////////////////////////////////////////////////////////////////////

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/USCrime/NYPD_Complaint_Data_Historic.csv'
INTO TABLE NYPDComplaint
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 1048477 LINES
(@_dummy, @_occurrence_date, @_dummy, @_dummy, @_dummy, @_reported_date, code, @_dummy, @_dummy, description, @_dummy, type, @_dummy, @_dummy, borough, precinct, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_dummy, @_latitude, @_longitude)
SET
    occurrence_date = CAST(@_occurrence_date AS DATE),
    reported_date = CAST(@_reported_date AS DATE),
    latitude = NULLIF(@_latitude, ''),
    longitude = NULLIF(@_longitude, '');

notee