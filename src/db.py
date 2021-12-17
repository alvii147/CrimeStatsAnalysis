import log
import utils

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

    values = utils.cleanRow(attributes.values())
    values = [f'{c}' if isinstance(c, int)  else c for c in values]
    values = ", ".join(values)

    query = 'INSERT INTO Person '
    query += f'({columns}) '
    query += f'VALUES ({values});'

    return query

print(insert(
    "Person",
    person_id = 1,
    age_range = "69-420",
    gender = "Apache Attack Helicopter",
    ethnicity = "Smurf"
))
