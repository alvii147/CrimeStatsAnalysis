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

closeDB(connection, cursor)
