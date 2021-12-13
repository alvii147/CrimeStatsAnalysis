import csv
import statistics

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