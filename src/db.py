import log
import utils

from decimal import Decimal

TABLES = utils.readJSON("tables.json")

def tableExists(table):
    return table in TABLES

def attributeExists(table, attribute):
    return attribute in TABLES[table]

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
    # values = utils.cleanRow(values)
    values = [f'{c}' if isinstance(c, int)  else c for c in values]
    values = [f'{c}' if isinstance(c, Decimal)  else c for c in values]
    values = ", ".join(values)


    query = f'INSERT INTO {table} '
    query += f'({columns}) '
    query += f'VALUES ({values});'

    return query
