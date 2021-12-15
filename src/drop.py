from utils import consoleFriendly
from MySQLutils import connectDB, closeDB

DROP_TABLE_QUERIES = [
'DROP TABLE IF EXISTS LondonStopAndSearch;',
'DROP TABLE IF EXISTS LondonOutcomes;',
'DROP TABLE IF EXISTS LondonStreet;',
'DROP TABLE IF EXISTS NYPDComplaints;',
'DROP TABLE IF EXISTS ChicagoCrimes;',
'DROP TABLE IF EXISTS LACrimes;',
]

connection, cursor = connectDB()

for query in DROP_TABLE_QUERIES:
    console_query = consoleFriendly(query)
    print(f'Executing query "{console_query}" ...')
    cursor.execute(query)

connection.commit()
closeDB(connection, cursor)