from decimal import Decimal
from datetime import date

from MySQLutils import connectDB, closeDB

if __name__ == '__main__':
    connection, cursor = connectDB()

    query = 'SELECT * FROM LondonStopAndSearch;'

    cursor.execute(query)
    LondonStopAndSearch = cursor.fetchall()

    for row in LondonStopAndSearch:
        row = [f'\'{c}\'' if isinstance(c, str)  else c for c in row]
        row = [f'\'{c}\'' if isinstance(c, date)  else c for c in row]
        row = ['NULL' if c is None  else c for c in row]

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

    closeDB(connection, cursor)