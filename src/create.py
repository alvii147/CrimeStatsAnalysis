from pathlib import Path
from MySQLutils import connectDB, closeDB

SQL_file_path = str(Path(__file__).parent / 'create.sql')

connection, cursor = connectDB()

query = f'SOURCE {SQL_file_path};'
cursor.execute()

connection.commit()
closeDB(connection, cursor)