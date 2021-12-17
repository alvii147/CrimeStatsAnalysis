import log

from utils import consoleFriendly, loadQueries
from MySQLutils import connectDB, closeDB

connection, cursor = connectDB()
queries = loadQueries("clean.sql")

for query in queries:
    console_query = consoleFriendly(query)
    log.info(f'Executing query "{console_query}" ...')
    cursor.execute(query)

connection.commit()
closeDB(connection, cursor)

log.success("Removed all tables from database")
