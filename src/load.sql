-- Load Tables with Data for Crime Database

\! rm -f output_load.txt
tee output_load.txt

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-stop-and-search.csv'
INTO TABLE LondonStopAndSearch
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\n'
IGNORE 1 LINES
(type, @raw_date, @dummy, @dummy, latitude, longitude, gender, age_range, @dummy, ethnicity, legislation, object, outcome, @raw_object_caused_outcome, @raw_clothing_removal)
SET occurrence_date = CAST(@raw_date AS DATE), object_caused_outcome = CAST(@raw_object_caused_outcome = 'True' AS UNSIGNED), clothing_removal = CAST(@raw_clothing_removal = 'True' AS UNSIGNED);

notee