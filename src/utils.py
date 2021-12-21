import csv
import log
import json

from datetime import date
from MySQLutils import connectDB, closeDB

def read_csv(filename, ignore=1):
    '''
    Read csv from file path.

    Parameters
    ----------
    filename : str or ``pathlib.Path`` object
        Path to csv file as string or ``pathlib.Path`` object.
    ignore : int
        Rows to ignore from the top.

    Returns
    -------
    data : list
        List containing each row as a tuple.
    '''

    datafile = csv.reader(open(filename))

    data = []
    for row in datafile:
        if ignore > 0:
            ignore -= 1
            continue

        data.append(row)

    return data

def readJSON(path):
    '''
    Read json from file path.

    Parameters
    ----------
    filename : str or ``pathlib.Path`` object
        Path to json file as string or ``pathlib.Path`` object.

    Returns
    -------
    data : dict
        Dictionary containing extracted json file.
    '''

    with open(path, "r") as file:
        return json.loads(file.read())

TABLES = readJSON("tables.json")

def isNull(s):
    '''
    Check if string is 'NULL'.

    Parameters
    ----------
    s : str
        Given string.

    Returns
    -------
    bool
        True if NULL, False if not NULL.
    '''

    return s == "\"NULL\"" or s == "\'NULL\'"

def isQuoted(s, quote='\''):
    '''
    Check if string is quoted.

    Parameters
    ----------
    s : str
        Given string.
    q : str
        Quote type to check for. Must be set to either ' or ".

    Returns
    -------
    bool
        True if quoted, False if not quoted.
    '''

    if quote not in ['\'', '"']:
        raise ValueError('quote must be \' or ".')

    return s.startswith(quote) and s.endswith(quote)

def stripQuotes(s, quote = "\'"):
    '''
    Strip one pair of quotes from string from start and end if quoted.

    Parameters
    ----------
    s : str
        Given string.

    Returns
    -------
    str:
        Processed string.
    '''

    if isQuoted(s, quote = quote):
        return s[1 : len(s) - 1]

    return s

def cleanRow(row):
    '''
    Clean list of tuples to preprocess for database insertion.

    Parameters
    ----------
    row : list
        Given list of tuples.

    Returns
    -------
    list
        Processed list of tuples.
    '''

    row = [
        json.dumps(c) if isinstance(c, str) else c
        for c in row
    ]
    row = [
        f'"{c}"' if isinstance(c, date) else c
        for c in row
    ]
    row = [
        'NULL' if isinstance(c, str) and isNull(c) else c
        for c in row
    ]
    row = [
        'NULL' if c is None else c
        for c in row
    ]

    return row

def consoleFriendly(s):
    '''
    Get console friendly slice of multi-line string.

    Parameters
    ----------
    s : str
        Given string.

    str
        Processed string.
    '''

    return list(filter(lambda x: len(x.strip()), s.split('\n')))[0]

def loadQueries(path):
    '''
    Load SQL queries from file path.

    Parameters
    ----------
    filename : str or ``pathlib.Path`` object
        Path to SQL file as string or ``pathlib.Path`` object.

    Returns
    -------
    queries : list
        List of loaded queries.
    '''

    with open(path, "r") as file:
        contents = file.read()

    queries = contents.split(';')
    # last element is always garbage (after last ';')
    queries = queries[:-1]

    for i in range(len(queries)):
        queries[i] = queries[i].strip('\n')

    log.success(f"Loaded {len(queries)} queries from '{path}'")
    return queries

def runQueries(path):
    '''
    Run SQL queries from file path.

    Parameters
    ----------
    filename : str or ``pathlib.Path`` object
        Path to SQL file as string or ``pathlib.Path`` object.
    '''

    connection, cursor = connectDB()
    queries = loadQueries(path)

    for query in queries:
        console_query = consoleFriendly(query)
        log.info(f'Executing query "{console_query}" ...')
        cursor.execute(query)

    connection.commit()
    closeDB(connection, cursor)

def yes(message):
    log.info(message)
    choice = ""

    while choice != "no" and choice != "yes":
        choice = input("[yes/no]: ").lower()

    if choice == "yes":
        return True
    else:
        return False

def no(message):
    return not yes(message)

def prompt_attribute(table, attribute):
    type = TABLES[table][attribute]
    value = input(f"[{type}] {attribute}: ")

    if isQuoted(value, quote = "\'"):
        value = stripQuotes(value, quote = "\'")
    elif isQuoted(value, quote = "\""):
        value = stripQuotes(value, quote = "\"")

    if value == "":
        value = 'NULL'

    return value

def prompt_table(table, ignore = []):
    log.info(f"{table}:")
    record = {}
    for attribute in TABLES[table]:
        if attribute in ignore:
            continue
        record[attribute] = prompt_attribute(table, attribute)
    return record

def prompt_table_update(table, ignore = []):
    log.info(f"{table}:")
    updates = {}   # new attribute values
    for attribute in TABLES[table]:
        if attribute in ignore:
            continue
        if yes(f"Update '{attribute}'?"):
            print(attribute)
            updates[attribute] = prompt_attribute(table, attribute)
    return updates

def prompt_options(options, message=None):
    if message is not None:
        log.info(message)

    for i, opt in enumerate(options):
        log.info(f'[{i + 1}] {opt}')

    log.info(f'[{len(options)}] Quit')

    selection_idx = int(input('Enter selection: ')) - 1
    if selection_idx > len(options):
        raise ValueError('Invalid selection')

    return selection_idx