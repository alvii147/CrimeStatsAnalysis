import log
import utils

from decimal import Decimal

TABLES = utils.readJSON("tables.json")

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

def select(table, where, attributes = None):
    if not tableExists(table):
        log.error(f"No such table '{table}'")
        return

    if attributes is None:
        project = "*"
    else:
        for a in attributes:
            if not attributeExists(table, a):
                log.error(f"No such attribute '{a}' in table '{table}'")
                return
        project = ", ".join(attributes)

    query = f'SELECT {project} FROM {table} WHERE {where};'
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
