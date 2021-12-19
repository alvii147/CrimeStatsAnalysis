import csv

def read_csv(filename, ignore=1):
    datafile = csv.reader(open(filename))

    data = []
    for row in datafile:
        if ignore > 0:
            ignore -= 1
            continue

        data.append(row)

    return data

LA_CRIME_CODES = {}

def addCodes(data):
    for row in data:
        code = row[8]
        description = row[9]

        if code not in LA_CRIME_CODES:
            LA_CRIME_CODES[code] = description
            print(f"{code}: {description}")

addCodes(read_csv("Crime_Data_from_2010_to_2019.csv"))
addCodes(read_csv("Crime_Data_from_2020_to_Present.csv"))

file = open("LA_Crime_Codes.csv", "w+")
file.write("Code,Description\n")

for code in LA_CRIME_CODES:
    file.write(f"{code},{LA_CRIME_CODES[code]}\n")

file.close()
