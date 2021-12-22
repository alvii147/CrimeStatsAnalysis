import re
import log
from decimal import Decimal

import utils
from MySQLutils import connectDB, closeDB

connection, cursor = connectDB()

TABLES_LIST = [
    'Crime',
    'Complaint',
    'Search',
    'Incident',
    'Location',
    'Code',
    'Person',
    'CrimeView',
    'ComplaintView',
    'SearchView',
]

TABLES = {}
for table in TABLES_LIST:
    query = 'SELECT '
    query += 'COLUMN_NAME, '
    query += 'DATA_TYPE, '
    query += 'CHARACTER_MAXIMUM_LENGTH, '
    query += 'NUMERIC_PRECISION, '
    query += 'NUMERIC_SCALE '
    query += 'FROM INFORMATION_SCHEMA.COLUMNS '
    query += f'WHERE TABLE_NAME=\'{table}\' AND TABLE_SCHEMA=DATABASE() '
    query += 'ORDER BY ORDINAL_POSITION ASC;'

    cursor.execute(query)
    output = cursor.fetchall()

    md = {}
    for row in output:
        column_name = row[0]
        data_type = row[1].decode("utf-8")
        if data_type.upper() == 'VARCHAR':
            md[column_name] = f'{data_type.upper()}({row[2]})'
        elif data_type.upper() == 'INT' or data_type.upper() == 'TINYINT':
            md[column_name] = f'{data_type.upper()}({row[3]})'
        elif data_type.upper() == 'DECIMAL':
            md[column_name] = f'{data_type.upper()}({row[3]}, {row[4]})'
        else:
            md[column_name] = data_type.upper()

    TABLES[table] = md

CSV_ENTRIES = {
    '/var/lib/mysql-files/10-Crime/UKCrime/london-stop-and-search.csv': 302624,
    '/var/lib/mysql-files/10-Crime/UKCrime/london-outcomes.csv': 1947051,
    '/var/lib/mysql-files/10-Crime/UKCrime/london-street.csv': 2946480,
    '/var/lib/mysql-files/10-Crime/USCrime/NYPD_Complaint_Data_Historic.csv': 1048576,
    '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2001_to_2004.csv': 1923517,
    '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2005_to_2007.csv': 1872346,
    '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2008_to_2011.csv': 2688712,
    '/var/lib/mysql-files/10-Crime/USCrime/Chicago_Crimes_2012_to_2017.csv': 1456715,
    '/var/lib/mysql-files/10-Crime/USCrime/Crime_Data_from_2010_to_2019.csv': 2118204,
    '/var/lib/mysql-files/10-Crime/USCrime/Crime_Data_from_2020_to_Present.csv' : 326214,
}

def tableStats():
    num_attributes = 0
    for table in TABLES:
        num_attributes += len(TABLES[table])
    log.debug(f"{num_attributes} attributes over {len(TABLES)} tables")

def tableExists(table):
    return table.upper().startswith('INFORMATION_SCHEMA') or table in TABLES

def attributeExists(table, attribute):
    return table.upper().startswith('INFORMATION_SCHEMA') or attribute in TABLES[table]

def enhancedCleanRow(row):
    row = utils.cleanRow(row)
    row = [f'{c}' if isinstance(c, int)  else c for c in row]
    row = [f'{c}' if isinstance(c, Decimal)  else c for c in row]
    return row

def insert(table, **attributes):
    if not tableExists(table):
        log.error(f"No such table '{table}'")
        return

    for a in attributes:
        if not attributeExists(table, a):
            log.error(f"No such attribute '{a}' in table '{table}'")
            return

    columns = ", ".join(attributes.keys())

    values = attributes.values()
    values = enhancedCleanRow(values)
    values = ", ".join(values)

    query = f'INSERT INTO {table} '
    query += f'({columns}) '
    query += f'VALUES ({values});'

    return query

def select(table, where=None, attributes = None, additional_clauses = ''):
    if not tableExists(table):
        log.error(f"No such table '{table}'")
        return

    if attributes is None or len(attributes) == 0:
        project = "*"
    else:
        for a in attributes:
            if not attributeExists(table, a):
                log.error(f"No such attribute '{a}' in table '{table}'")
                return
        project = ", ".join(attributes)

    if where is None:
        query = f'SELECT {project} FROM {table} {additional_clauses};'
    else:
        query = f'SELECT {project} FROM {table} WHERE {where} {additional_clauses};'

    return query

def delete(table, where):
    if not tableExists(table):
        log.error(f"No such table '{table}'")
        return

    query = f'DELETE FROM {table} WHERE {where};'
    return query

def update(table, where, **attributes):
    if not tableExists(table):
        log.error(f"No such table '{table}'")
        return

    for a in attributes:
        if not attributeExists(table, a):
            log.error(f"No such attribute '{a}' in table '{table}'")
            return

    columns = list(attributes.keys())
    values = enhancedCleanRow(attributes.values())

    updates = []
    for i in range(len(columns)):
        updates.append(f"{columns[i]} = {values[i]}")
    updates = ", ".join(updates)

    query = f'UPDATE {table} SET {updates} WHERE {where};'
    return query

def getIgnoreLines(n, path, safety_net=10):
    entries = CSV_ENTRIES.get(path, 100)
    ignore_lines = entries - n

    if ignore_lines < safety_net:
        ignore_lines = safety_net
    elif ignore_lines > entries - safety_net:
        ignore_lines = entries - safety_net

    log.debug(f'n = {n}')
    log.debug(f'Ignoring {ignore_lines} lines from {path}')

    return ignore_lines

def loadReplaceIgnoreLines(query, n):
    rgx = r'LOAD\s+DATA\s+INFILE\s+(\S+)'
    path = re.search(rgx, query).group(1).strip('\'""')

    ignore_lines = getIgnoreLines(n, path)
    rgx = r'IGNORE\s+\d+\s+LINES'
    replace_str = f'IGNORE {ignore_lines} LINES'
    new_query = str(re.subn(rgx, replace_str, query, count=1, flags=re.IGNORECASE)[0])

    return new_query

closeDB(connection, cursor)
