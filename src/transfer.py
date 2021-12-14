from decimal import Decimal
from datetime import date
from MySQLutils import connectDB, closeDB

def cleanRow(row):
    row = [f'\'{c}\'' if isinstance(c, str)  else c for c in row]
    row = [f'\'{c}\'' if isinstance(c, date)  else c for c in row]
    row = ['NULL' if c is None  else c for c in row]

    return row

connection, cursor = connectDB()

# -------------------------
# London Stop & Search Data
# -------------------------

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
    query += f'VALUES ({incident_id}, {suspect_id}, {row[7]}, {row[8]}, {row[9]}, {row[10]}, {row[11]})'

    cursor.execute(query)

# ---------------
# London Outcomes
# ---------------

query = 'SELECT * FROM LondonOutcomes;'

cursor.execute(query)
LondonOutcomes = cursor.fetchall()

for row in LondonOutcomes:
    row = cleanRow(row)

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, lsoa_code city, country) '
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
    query += f'VALUES ({incident_id}, {row[5]})'

    cursor.execute(query)

# -------------
# London Street
# -------------

query = 'SELECT * FROM LondonStreet;'

cursor.execute(query)
LondonStreet = cursor.fetchall()

for row in LondonStreet:
    row = cleanRow(row)

    query = 'INSERT INTO Location '
    query += '(latitude, longitude, precinct, lsoa_code city, country) '
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
    query += f'VALUES ({incident_id}, {row[6]})'

    cursor.execute(query)

connection.commit()
closeDB(connection, cursor)