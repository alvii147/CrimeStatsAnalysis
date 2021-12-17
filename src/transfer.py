from pathlib import Path
from utils import read_csv, cleanRow
from MySQLutils import connectDB, closeDB
import log

connection, cursor = connectDB()

# -----------
# Crime Codes
# -----------

log.info('Inserting NYPD Crime Codes ...')
NYPD = read_csv(Path(__file__).parent / 'NYPD_Crime_Codes.csv')

for row in NYPD:
    row = cleanRow(row)

    query = 'INSERT INTO Code '
    query += '(code, organization, category) '
    query += f'VALUES ({row[0]}, \'NYPD\', {row[1]});'

    cursor.execute(query)

log.info('Inserting IUCR Crime Codes ...')
IUCR = read_csv(Path(__file__).parent / 'IUCR_Crime_Codes.csv')

for row in IUCR:
    row = cleanRow(row)

    query = 'INSERT INTO Code '
    query += '(code, organization, category, description) '
    query += f'VALUES ({row[0]}, \'IUCR\', {row[1]}, {row[2]});'

    cursor.execute(query)

log.info('Inserting UCR Crime Codes ...')
UCR = read_csv(Path(__file__).parent / 'UCR_Crime_Codes.csv')

for row in UCR:
    row = cleanRow(row)

    query = 'INSERT INTO Code '
    query += '(code, organization, category, description) '
    query += f'VALUES ({row[0]}, \'UCR\', {row[2]}, {row[1]});'

    cursor.execute(query)

# --------------------
# London Stop & Search
# --------------------

log.info('Transferring London Stop & Search Data ...')
query = 'SELECT * FROM LondonStopAndSearch;'

cursor.execute(query)
LondonStopAndSearch = cursor.fetchall()

for row in LondonStopAndSearch:
    row = cleanRow(row)

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, city, country) '
    query += f'VALUES ({row[2]}, {row[3]}, \'London\', \'United Kingdom\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date, type) '
    query += f'VALUES ({location_id}, {row[1]}, {row[0]});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Person '
    query += '(age_range, gender, ethnicity) '
    query += f'VALUES ({row[4]}, {row[5]}, {row[6]});'

    cursor.execute(query)
    suspect_id = cursor.lastrowid

    query = 'INSERT INTO Search '
    query += '(incident_id, suspect_id, legislation, object, outcome, object_caused_outcome, clothing_removal) '
    query += f'VALUES ({incident_id}, {suspect_id}, {row[7]}, {row[8]}, {row[9]}, {row[10]}, {row[11]});'

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

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, lsoa_code, city, country) '
    query += f'VALUES ({row[1]}, {row[2]}, {row[3]}, {row[4]}, \'London\', \'United Kingdom\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date) '
    query += f'VALUES ({location_id}, {row[0]});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Crime '
    query += '(incident_id, description) '
    query += f'VALUES ({incident_id}, {row[5]});'

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

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, lsoa_code, city, country) '
    query += f'VALUES ({row[1]}, {row[2]}, {row[3]}, {row[4]}, \'London\', \'United Kingdom\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date, type) '
    query += f'VALUES ({location_id}, {row[0]}, {row[5]});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Crime '
    query += '(incident_id, description) '
    query += f'VALUES ({incident_id}, {row[6]});'

    cursor.execute(query)

# ---------------
# NYPD Complaints
# ---------------

log.info('Transferring NYPD Complaints Data ...')
query = 'SELECT * FROM NYPDComplaints;'

cursor.execute(query)
NYPDComplaints = cursor.fetchall()

for row in NYPDComplaints:
    row = cleanRow(row)

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, borough, city, state, country) '
    query += f'VALUES ({row[4]}, {row[5]}, {row[6]}, {row[7]}, \'New York\', \'New York\', \'United States\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date, type) '
    query += f'VALUES ({location_id}, {row[0]}, {row[8]});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    code = row[2]
    organization = '\'NYPD\''
    if row[2].strip('\'') not in [i[0] for i in NYPD]:
        code = 'NULL'
        organization = 'NULL'

    query = 'INSERT INTO Complaint '
    query += '(incident_id, code, organization, reported_date, description) '
    query += f'VALUES ({incident_id}, {code}, {organization}, {row[1]}, {row[9]});'

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

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, borough, city, state, country) '
    query += f'VALUES ({row[3]}, {row[4]}, {row[5]}, {row[6]}, \'Chicago\', \'Illinois\', \'United States\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date) '
    query += f'VALUES ({location_id}, {row[0]});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    code = row[1]
    organization = '\'IUCR\''
    if row[1].strip('\'') not in [i[0] for i in IUCR]:
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

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, city, state, country) '
    query += f'VALUES ({row[3]}, {row[4]}, \'Los Angeles\', \'California\', \'United States\');'

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = 'INSERT INTO Incident '
    query += '(location_id, occurrence_date) '
    query += f'VALUES ({location_id}, {row[0]});'

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = 'INSERT INTO Person '
    query += '(age_range, gender, ethnicity) '
    query += f'VALUES ({row[5]}, {row[6]}, {row[7]});'

    cursor.execute(query)
    victim_id = cursor.lastrowid

    code = row[1]
    organization = '\'UCR\''
    if row[1].strip('\'') not in [i[0] for i in UCR]:
        code = 'NULL'
        organization = 'NULL'

    query = 'INSERT INTO Crime '
    query += '(incident_id, code, organization, victim_id) '
    query += f'VALUES ({incident_id}, {code}, {organization}, {victim_id});'

    cursor.execute(query)

connection.commit()
closeDB(connection, cursor)