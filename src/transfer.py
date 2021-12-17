from typing import OrderedDict
import log
import db

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

    code                = row[0]
    offence_description = row[1]

    query = db.insert(
        'Code',
        code = code,
        organization = 'NYPD',
        category = offence_description
    )

    cursor.execute(query)

log.info('Inserting IUCR Crime Codes ...')
IUCR = read_csv(Path(__file__).parent / 'IUCR_Crime_Codes.csv')

for row in IUCR:
    row = cleanRow(row)

    code                  = row[0]
    primary_description   = row[1]
    secondary_description = row[2]
    index_code            = row[3]

    query = db.insert(
        'Code',
        code = code,
        organization = 'IUCR',
        category = primary_description,
        description = secondary_description
    )

    cursor.execute(query)

log.info('Inserting UCR Crime Codes ...')
UCR = read_csv(Path(__file__).parent / 'UCR_Crime_Codes.csv')

for row in UCR:
    row = cleanRow(row)

    code        = row[0]
    description = row[1]
    category    = row[2]

    query = db.insert(
        'Code',
        code = code,
        organization = 'UCR',
        category = category,
        description = description
    )

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
log.note("LSOA names are only for UK?")
log.note("Can we put LSOA/borough in Location?")

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

    query = db.insert(
        'Location',
        latitude = latitude,
        longitude = longitude,
        city = 'London',
        country = 'United Kingdom'
    )

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = db.insert(
        'Incident',
        location_id = location_id,
        occurrence_date = occurrence_date,
        type = type
    )

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = db.insert(
        'Person',
        age_range = age_range,
        gender = gender,
        ethnicity = ethnicity
    )

    cursor.execute(query)
    suspect_id = cursor.lastrowid

    query = db.insert(
        'Search',
        incident_id = incident_id,
        suspect_id = suspect_id,
        legislation = legislation,
        object = object,
        outcome = outcome,
        object_caused_outcome = object_caused_outcome,
        clothing_removal = clothing_removal
    )

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

    query = db.insert(
        'Location',
        latitude = latitude,
        longitude = longitude,
        precinct = precinct,
        lsoa_code = lsoa_code,
        city = 'London',
        country = 'United Kingdom'
    )

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = db.insert(
        'Incident',
        location_id = location_id,
        occurrence_date = occurrence_date
    )

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = db.insert(
        'Crime',
        incident_id = incident_id,
        description = description
    )

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

    query = db.insert(
        'Location',
        latitude = latitude,
        longitude = longitude,
        precinct = precinct,
        lsoa_code = lsoa_code,
        city = 'London',
        country = 'United Kingdom'
    )

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = db.insert(
        'Incident',
        location_id = location_id,
        occurrence_date = occurrence_date,
        type = type
    )

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = db.insert(
        'Crime',
        incident_id = incident_id,
        description = description
    )

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

    query = db.insert(
        'Location',
        latitude = latitude,
        longitude = longitude,
        precinct = precinct,
        borough = borough,
        city = 'New York',
        state = 'New York',
        country = 'United States'
    )

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = db.insert(
        'Incident',
        location_id = location_id,
        occurrence_date = occurrence_date,
        type = type
    )

    cursor.execute(query)
    incident_id = cursor.lastrowid

    organization = '\'NYPD\''
    if code.strip('\'') not in [i[0] for i in NYPD]:
        code = 'NULL'
        organization = 'NULL'

    query = db.insert(
        'Complaint',
        incident_id = incident_id,
        code = code,
        organization = organization,
        reported_date = reported_date,
        description = description
    )

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

    query = db.insert(
        'Location',
        latitude = latitude,
        longitude = longitude,
        precinct = precinct,
        borough = borough,
        city = 'Chicago',
        state = 'Illinois',
        country = 'United States'
    )

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = db.insert(
        'Incident',
        location_id = location_id,
        occurrence_date = occurrence_date
    )

    cursor.execute(query)
    incident_id = cursor.lastrowid

    organization = '\'IUCR\''
    if code.strip('\'') not in [i[0] for i in IUCR]:
        code = 'NULL'
        organization = 'NULL'

    query = db.insert(
        'Crime',
        incident_id = incident_id,
        code = code,
        organization = organization
    )

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

    query = db.insert(
        'Location',
        latitude = latitude,
        longitude = longitude,
        city = 'Los Angeles',
        state = 'California',
        country = 'United States'
    )

    cursor.execute(query)
    location_id = cursor.lastrowid

    query = db.insert(
        'Incident',
        location_id = location_id,
        occurrence_date = occurrence_date
    )

    cursor.execute(query)
    incident_id = cursor.lastrowid

    query = db.insert(
        'Person',
        age_range = age_range,
        gender = gender,
        ethnicity = ethnicity
    )

    cursor.execute(query)
    victim_id = cursor.lastrowid

    organization = '\'UCR\''
    if code.strip('\'') not in [i[0] for i in UCR]:
        code = 'NULL'
        organization = 'NULL'

    query = db.insert(
        'Crime',
        incident_id = incident_id,
        code = code,
        organization = organization,
        victim_id = victim_id
    )

    cursor.execute(query)

connection.commit()
closeDB(connection, cursor)
