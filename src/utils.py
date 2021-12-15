import csv
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

def cleanRow(row):
    row = [f'\'{c}\'' if isinstance(c, str)  else c for c in row]
    row = [f'\'{c}\'' if isinstance(c, date)  else c for c in row]
    row = ['NULL' if c is None  else c for c in row]

    return row

def consoleFriendly(s):
    return list(filter(lambda x: len(x.strip()), s.split('\n')))[0]