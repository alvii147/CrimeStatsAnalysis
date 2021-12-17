import log

from pathlib import Path
from utils import read_csv, cleanRow
from MySQLutils import connectDB, closeDB

connection, cursor = connectDB()

# -----------
# Crime Codes
# -----------

log.info('Inserting NYPD Crime Codes ...')
NYPD = read_csv(Path(__file__).parent / 'NYPD_Crime_Codes.csv')

for row in NYPD:
    row = cleanRow(row)

    key_code            = row[0]
    offence_description = row[1]

    query = 'INSERT INTO Code '
    query += '(code, organization, category) '
    query += f'VALUES ({key_code}, \'NYPD\', {offence_description});'

    cursor.execute(query)

log.info('Inserting IUCR Crime Codes ...')
IUCR = read_csv(Path(__file__).parent / 'IUCR_Crime_Codes.csv')

for row in IUCR:
    row = cleanRow(row)

    IUCR_code             = row[0]
    primary_description   = row[1]
    secondary_description = row[2]
    index_code            = row[3]

    query = 'INSERT INTO Code '
    query += '(code, organization, category, description) '
    query += f'VALUES ({IUCR_code}, \'IUCR\', {primary_description}, {secondary_description});'

    cursor.execute(query)

log.info('Inserting UCR Crime Codes ...')
UCR = read_csv(Path(__file__).parent / 'UCR_Crime_Codes.csv')

for row in UCR:
    row = cleanRow(row)

    code        = row[0]
    description = row[1]
    category    = row[2]

    query = 'INSERT INTO Code '
    query += '(code, organization, category, description) '
    query += f'VALUES ({code}, \'UCR\', {category}, {description});'

    cursor.execute(query)

# --------------------
# London Stop & Search
# --------------------

log.info('Transferring London Stop & Search Data ...')
query = 'SELECT * FROM LondonStopAndSearch;'

cursor.execute(query)
LondonStopAndSearch = cursor.fetchall()

log.note("How do we deal with duplicate locations?")
log.note("Won't the IDs increment automatically?")

for row in LondonStopAndSearch:
    row = cleanRow(row)

    type                  = row[0]
    occurrence_date       = row[1]
    latitude              = row[2]
    longitude             = row[3]
    age_range             = row[4]
    gender                = row[5]
    ethnicity             = row[6]
    legislation           = row[7]
    object                = row[8]
    outcome               = row[9]
    object_caused_outcome = row[10]
    clothing_removal      = row[11]

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, city, country) '
    query += f'VALUES ({latitude}, {longitude}, \'London\', \'United Kingdom\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date, type) '
    query += f'VALUES ({location_id}, {occurrence_date}, {type});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Person '
    query += '(age_range, gender, ethnicity) '
    query += f'VALUES ({age_range}, {gender}, {ethnicity});'

    cursor.execute(query)
    suspect_id = cursor.lastrowid

    query = 'INSERT INTO Search '
    query += '(incident_id, suspect_id, legislation, object, outcome, object_caused_outcome, clothing_removal) '
    query += f'VALUES ({incident_id}, {suspect_id}, {legislation}, {object}, {outcome}, {object_caused_outcome}, {clothing_removal});'

    cursor.execute(query)

# ---------------
# London Outcomes
# ---------------

log.info('Transferring London Outcomes Data ...')
query = 'SELECT * FROM LondonOutcomes;'

cursor.execute(query)
LondonOutcomes = cursor.fetchall()

for row in LondonOutcomes:
    row = cleanRow(row)

    occurrence_date  = row[0]
    latitude         = row[1]
    longitude        = row[2]
    precinct         = row[3]
    lsoa_code        = row[4]
    description      = row[5]

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, lsoa_code, city, country) '
    query += f'VALUES ({latitude}, {longitude}, {precinct}, {lsoa_code}, \'London\', \'United Kingdom\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date) '
    query += f'VALUES ({location_id}, {occurrence_date});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Crime '
    query += '(incident_id, description) '
    query += f'VALUES ({incident_id}, {description});'

    cursor.execute(query)

# -------------
# London Street
# -------------

log.info('Transferring London Street Data ...')
query = 'SELECT * FROM LondonStreet;'

cursor.execute(query)
LondonStreet = cursor.fetchall()

for row in LondonStreet:
    row = cleanRow(row)

    occurrence_date  = row[0]
    latitude         = row[1]
    longitude        = row[2]
    precinct         = row[3]
    lsoa_code        = row[4]
    type             = row[5]
    description      = row[6]

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, lsoa_code, city, country) '
    query += f'VALUES ({latitude}, {longitude}, {precinct}, {lsoa_code}, \'London\', \'United Kingdom\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date, type) '
    query += f'VALUES ({location_id}, {occurrence_date}, {type});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Crime '
    query += '(incident_id, description) '
    query += f'VALUES ({incident_id}, {description});'

    cursor.execute(query)
log.note("fix ER disgram for occurrance date")
log.note("fix reported date column name")
log.note("investigate LSOA names (neighbourhoods / boroughs")
# ---------------
# NYPD Complaints
# ---------------

log.info('Transferring NYPD Complaints Data ...')
query = 'SELECT * FROM NYPDComplaints;'

cursor.execute(query)
NYPDComplaints = cursor.fetchall()

for row in NYPDComplaints:
    row = cleanRow(row)

    occurrence_date = row[0]
    reported_date   = row[1]
    code            = row[2]
    organization    = row[3]
    latitude        = row[4]
    longitude       = row[5]
    precinct        = row[6]
    borough         = row[7]
    type            = row[8]
    description     = row[9]

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, borough, city, state, country) '
    query += f'VALUES ({latitude}, {longitude}, {precinct}, {borough}, \'New York\', \'New York\', \'United States\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date, type) '
    query += f'VALUES ({location_id}, {occurrence_date}, {type});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    organization = '\'NYPD\''
    if code.strip('\'') not in [i[0] for i in NYPD]:
        code = 'NULL'
        organization = 'NULL'

    query = 'INSERT INTO Complaint '
    query += '(incident_id, code, organization, reported_date, description) '
    query += f'VALUES ({incident_id}, {code}, {organization}, {reported_date}, {description});'

    cursor.execute(query)

# --------------
# Chicago Crimes
# --------------

log.info('Transferring Chicago Crimes Data ...')
query = 'SELECT * FROM ChicagoCrimes;'

cursor.execute(query)
ChicagoCrimes = cursor.fetchall()

for row in ChicagoCrimes:
    row = cleanRow(row)

    occurrence_date = row[0]
    code            = row[1]
    organization    = row[2]
    latitude        = row[3]
    longitude       = row[4]
    precinct        = row[5]
    borough         = row[6]

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, borough, city, state, country) '
    query += f'VALUES ({latitude}, {longitude}, {precinct}, {borough}, \'Chicago\', \'Illinois\', \'United States\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date) '
    query += f'VALUES ({location_id}, {occurrence_date});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    organization = '\'IUCR\''
    if code.strip('\'') not in [i[0] for i in IUCR]:
        code = 'NULL'
        organization = 'NULL'

    query = 'INSERT INTO Crime '
    query += '(incident_id, code, organization) '
    query += f'VALUES ({incident_id}, {code}, {organization});'

    cursor.execute(query)

# ---------
# LA Crimes
# ---------

log.info('Transferring LA Crimes Data ...')
query = 'SELECT * FROM LACrimes;'

cursor.execute(query)
LACrimes = cursor.fetchall()

for row in LACrimes:
    row = cleanRow(row)

    occurrence_date = row[0]
    code            = row[1]
    organization    = row[2]
    latitude        = row[3]
    longitude       = row[4]
    age_range       = row[5]
    gender          = row[6]
    ethnicity       = row[7]

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, city, state, country) '
    query += f'VALUES ({latitude}, {longitude}, \'Los Angeles\', \'California\', \'United States\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date) '
    query += f'VALUES ({location_id}, {occurrence_date});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Person '
    query += '(age_range, gender, ethnicity) '
    query += f'VALUES ({age_range}, {gender}, {ethnicity});'

    cursor.execute(query)
    victim_id = cursor.lastrowid

    organization = '\'UCR\''
    if code.strip('\'') not in [i[0] for i in UCR]:
        code = 'NULL'
        organization = 'NULL'

    query = 'INSERT INTO Crime '
    query += '(incident_id, code, organization, victim_id) '
    query += f'VALUES ({incident_id}, {code}, {organization}, {victim_id});'

    cursor.execute(query)

connection.commit()
closeDB(connection, cursor)
