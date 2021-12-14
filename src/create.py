from pathlib import Path
from MySQLutils import connectDB, closeDB

path = str(Path(__file__).parent.resolve() / 'create.sql')
with open(path, 'r') as SQLfilepath:
    query = SQLfilepath.read()

connection, cursor = connectDB()

cursor.execute(query)

connection.commit()
closeDB(connection, cursor)