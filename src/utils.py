import csv
import log
import json

from datetime import date

def read_csv(filename):
    datafile = csv.reader(open(filename))

    first_row = True
    data = []
    for row in datafile:
        if first_row:
            first_row = False
            continue

        data.append(row)

    return data

def isNull(s):
    return s == "\"NULL\"" or s == "\'NULL\'"

def isQuoted(s):
    return (s.startswith("\"") and s.endswith("\"")) or (s.startswith("\'") and s.endswith("\'"))

def cleanRow(row):
    row = [f'\'{c}\'' if isinstance(c, str) and not isQuoted(c)  else c for c in row]
    row = [f'\'{c}\'' if isinstance(c, date)  else c for c in row]
    row = ['NULL' if isinstance(c, str) and isNull(c)  else c for c in row]
    row = ['NULL' if c is None  else c for c in row]

    return row

def consoleFriendly(s):
    return list(filter(lambda x: len(x.strip()), s.split('\n')))[0]

def loadQueries(path):
    with open(path, "r") as file:
        contents = file.read()

    queries = contents.split(';')
    queries = queries[:-1]   # last element is always garbage (after last ';')

    for i in range(len(queries)):
        queries[i] = queries[i].strip('\n')

    log.success(f"Loaded {len(queries)} queries from '{path}'")
    return queries

def readJSON(path):
    with open(path, "r") as file:
        return json.loads(file.read())
