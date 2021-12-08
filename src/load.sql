-- Load Tables with Data for Crime Database

\! rm -f output_load.txt
tee output_load.txt

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-police-records/london-stop-and-search.csv'
INTO TABLE Location
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\r\n'
IGNORE 1 LINES
(@dummy, @dummy, @dummy, @dummy, latitude, longitude)
SET country='United Kingdom';

notee