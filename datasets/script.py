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

filename = 'london-police-records/london-stop-and-search.csv'
data = read_csv(filename)

field_idx = 12
field = [row[field_idx] for row in data]
field_len = [len(row) for row in field]

print('median length', statistics.median(field_len))
print('max length', max(field_len))