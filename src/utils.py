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

def isQuoted(s):
    '''
    Check if string is quoted.

    Parameters
    ----------
    s : str
        Given string.

    Returns
    -------
    bool
        True if quoted, False if not quoted.
    '''

    return (
        (
            s.startswith("\"") and s.endswith("\"")
        ) or
        (
            s.startswith("\'") and s.endswith("\'")
        )
    )

def stripQuotes(s):
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

    if isQuoted(s):
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
        c.replace('\'', '') if isinstance(c, str) else c
        for c in row
    ]
    row = [
        f'\'{c}\'' if isinstance(c, str) and not isQuoted(c) else c
        for c in row
    ]
    row = [
        f'\'{c}\'' if isinstance(c, date) else c
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
