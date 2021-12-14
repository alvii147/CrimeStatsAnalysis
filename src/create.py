from pathlib import Path
from MySQLutils import connectDB, closeDB

SQL_file_path = str(Path(__file__).parent.resolve() / 'create.sql')

connection, cursor = connectDB()

query = f'SOURCE {SQL_file_path};'
cursor.execute(query)

connection.commit()
closeDB(connection, cursor)