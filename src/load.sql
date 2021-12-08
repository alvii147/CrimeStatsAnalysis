-- Load Tables with Data for Crime Database

\! rm -f output_load.txt
tee output_load.txt

LOAD DATA INFILE '/var/lib/mysql-files/10-Crime/UKCrime/london-stop-and-search.csv'
INTO TABLE Location
(@dummy, @dummy, @dummy, @dummy, latitude, longitude)
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES
    TERMINATED BY '\r\n'
IGNORE 1 LINES
SET country='United Kingdom';

notee