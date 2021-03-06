import log
import db
import person

from pathlib import Path
from utils import read_csv
from MySQLutils import connectDB, closeDB

def transfer_all():
    connection, cursor = connectDB()

    # -----------
    # Crime Codes
    # -----------

    log.info('Inserting NYPD Crime Codes ...')
    NYPD = read_csv(Path(__file__).parent / 'codes/NYPD_Crime_Codes.csv')

    for row in NYPD:
        code                = row[0]
        offence_description = row[1]

        query = db.insert(
            'Code',
            code = code,
            organization = 'NYPD',
            category = offence_description
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Code')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    log.info('Inserting IUCR Crime Codes ...')
    IUCR = read_csv(Path(__file__).parent / 'codes/IUCR_Crime_Codes.csv')

    for row in IUCR:
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

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Code')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    log.info('Inserting UCR Crime Codes ...')
    UCR = read_csv(Path(__file__).parent / 'codes/UCR_Crime_Codes.csv')

    for row in UCR:
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

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Code')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    log.info('Inserting LA Crime Codes ...')
    LAPD = read_csv(Path(__file__).parent / 'codes/LAPD_Crime_Codes.csv')

    for row in LAPD:
        code        = row[0]
        description = row[1]

        query = db.insert(
            'Code',
            code = code,
            organization = 'LAPD',
            description = description
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Code')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    log.info('Transferring London Stop & Search Data ...')
    query = 'SELECT * FROM LondonStopAndSearch;'

    cursor.execute(query)
    LondonStopAndSearch = cursor.fetchall()

    for row in LondonStopAndSearch:
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

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Location')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        location_id = cursor.lastrowid

        query = db.insert(
            'Incident',
            location_id = location_id,
            occurrence_date = occurrence_date,
            police_department = 'City of London Police',
            type = type
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Incident')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        incident_id = cursor.lastrowid

        first_name, last_name, phone_number = person.info(gender)

        query = db.insert(
            'Person',
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            age_range = age_range,
            gender = gender,
            ethnicity = ethnicity
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Person')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

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

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Search')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    # ---------------
    # London Outcomes
    # ---------------

    log.info('Transferring London Outcomes Data ...')
    query = 'SELECT * FROM LondonOutcomes;'

    cursor.execute(query)
    LondonOutcomes = cursor.fetchall()

    for row in LondonOutcomes:
        occurrence_date   = row[0]
        latitude          = row[1]
        longitude         = row[2]
        borough           = row[3]
        description       = row[4]
        police_department = row[5]
        area              = row[6]

        query = db.insert(
            'Location',
            latitude = latitude,
            longitude = longitude,
            borough = borough,
            area = area,
            city = 'London',
            country = 'United Kingdom'
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Location')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        location_id = cursor.lastrowid

        query = db.insert(
            'Incident',
            location_id = location_id,
            police_department = police_department,
            occurrence_date = occurrence_date
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Incident')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        incident_id = cursor.lastrowid

        query = db.insert(
            'Crime',
            incident_id = incident_id,
            description = description
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Crime')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    # -------------
    # London Street
    # -------------

    log.info('Transferring London Street Data ...')
    query = 'SELECT * FROM LondonStreet;'

    cursor.execute(query)
    LondonStreet = cursor.fetchall()

    for row in LondonStreet:
        occurrence_date   = row[0]
        latitude          = row[1]
        longitude         = row[2]
        borough           = row[3]
        type              = row[4]
        description       = row[5]
        police_department = row[6]
        area              = row[7]

        query = db.insert(
            'Location',
            latitude = latitude,
            longitude = longitude,
            borough = borough,
            area = area,
            city = 'London',
            country = 'United Kingdom'
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Location')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        location_id = cursor.lastrowid

        query = db.insert(
            'Incident',
            location_id = location_id,
            occurrence_date = occurrence_date,
            police_department = police_department,
            type = type
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Incident')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        incident_id = cursor.lastrowid

        query = db.insert(
            'Crime',
            incident_id = incident_id,
            description = description
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Crime')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    # ---------------
    # NYPD Complaints
    # ---------------

    log.info('Transferring NYPD Complaints Data ...')
    query = 'SELECT * FROM NYPDComplaints;'

    cursor.execute(query)
    NYPDComplaints = cursor.fetchall()

    for row in NYPDComplaints:
        occurrence_date = row[0]
        reported_date   = row[1]
        code            = row[2]
        organization    = row[3]
        latitude        = row[4]
        longitude       = row[5]
        premises        = row[6]
        precinct        = row[7]
        borough         = row[8]
        type            = row[9]
        description     = row[10]
        area            = row[11]

        query = db.insert(
            'Location',
            latitude = latitude,
            longitude = longitude,
            premises = premises,
            area = area,
            precinct = precinct,
            borough = borough,
            city = 'New York',
            state = 'New York',
            country = 'United States'
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Location')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        location_id = cursor.lastrowid

        query = db.insert(
            'Incident',
            location_id = location_id,
            occurrence_date = occurrence_date,
            police_department = 'New York Police Department',
            type = type
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Incident')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        incident_id = cursor.lastrowid

        organization = 'NYPD'
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

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Complaint')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    # --------------
    # Chicago Crimes
    # --------------

    log.info('Transferring Chicago Crimes Data ...')
    query = 'SELECT * FROM ChicagoCrimes;'

    cursor.execute(query)
    ChicagoCrimes = cursor.fetchall()

    for row in ChicagoCrimes:
        occurrence_date = row[0]
        code            = row[1]
        organization    = row[2]
        latitude        = row[3]
        longitude       = row[4]
        ward            = row[5]
        borough         = row[6]
        area            = row[7]
        last_updated    = row[8]
        domestic        = row[9]

        query = db.insert(
            'Location',
            latitude = latitude,
            longitude = longitude,
            ward = ward,
            borough = borough,
            area = area,
            city = 'Chicago',
            state = 'Illinois',
            country = 'United States'
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Location')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        location_id = cursor.lastrowid

        query = db.insert(
            'Incident',
            location_id = location_id,
            last_updated = last_updated,
            police_department = 'Chicago Police Department',
            occurrence_date = occurrence_date
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Incident')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        incident_id = cursor.lastrowid

        organization = 'IUCR'
        if code.strip('\'') not in [i[0] for i in IUCR]:
            code = 'NULL'
            organization = 'NULL'

        query = db.insert(
            'Crime',
            incident_id = incident_id,
            code = code,
            domestic = domestic,
            organization = organization
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Crime')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    # ---------
    # LA Crimes
    # ---------

    log.info('Transferring LA Crimes Data ...')
    query = 'SELECT * FROM LACrimes;'

    cursor.execute(query)
    LACrimes = cursor.fetchall()

    for row in LACrimes:
        occurrence_date = row[0]
        code            = row[1]
        organization    = row[2]
        latitude        = row[3]
        longitude       = row[4]
        age_range       = row[5]
        gender          = row[6]
        ethnicity       = row[7]
        weapon          = row[8]
        premises        = row[9]
        precinct        = row[10]
        borough         = row[11]
        area            = row[12]
        status          = row[13]

        query = db.insert(
            'Location',
            latitude = latitude,
            longitude = longitude,
            city = 'Los Angeles',
            state = 'California',
            country = 'United States',
            premises = premises,
            area = area,
            precinct = precinct,
            borough = borough
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Location')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        location_id = cursor.lastrowid

        query = db.insert(
            'Incident',
            location_id = location_id,
            police_department = 'Los Angeles Police Department',
            status = status,
            occurrence_date = occurrence_date
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Incident')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        incident_id = cursor.lastrowid

        first_name, last_name, phone_number = person.info(gender)

        query = db.insert(
            'Person',
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            age_range = age_range,
            gender = gender,
            ethnicity = ethnicity
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Person')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

        victim_id = cursor.lastrowid

        organization = 'LAPD'
        if code.strip('\'') not in [i[0] for i in LAPD]:
            code = 'NULL'
            organization = 'NULL'

        query = db.insert(
            'Crime',
            incident_id = incident_id,
            code = code,
            organization = organization,
            victim_id = victim_id,
            weapon = weapon
        )

        try:
            cursor.execute(query)
        except Exception as e:
            log.error('Unable to insert row into table Crime')
            log.error('Row contents:')
            log.error(row)
            log.error('Exception:')
            log.error(e)
            log.error('Skipping row')
            continue

    connection.commit()
    closeDB(connection, cursor)
