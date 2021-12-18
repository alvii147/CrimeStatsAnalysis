# This script filters out only the London borough LSOAs from UK_Regions.csv

import log

from utils import read_csv

INPUT_CSV = "region_data/UK_Regions.csv"
OUTPUT_CSV = "region_data/London_Boroughs.csv"

UK_REGIONS = read_csv(INPUT_CSV)
LSOA_BOROUGHS = {}

lsoa_count = 0
borough_count = 0

for row in UK_REGIONS:
	borough = row[2]
	lsoa = row[3]

	if "London" not in ",".join(row):
		continue

	if borough not in LSOA_BOROUGHS.values():
		borough_count += 1
		log.debug(borough)

	if lsoa not in LSOA_BOROUGHS:
		LSOA_BOROUGHS[lsoa] = borough
		lsoa_count += 1

log.success(f"Found {lsoa_count} LSOAs among {borough_count} boroughs in London")

with open(OUTPUT_CSV, "w") as file:
	file.write("LSOA,Borough\n")
	for lsoa in LSOA_BOROUGHS:
		file.write(f"{lsoa},{LSOA_BOROUGHS[lsoa]}\n")

log.success(f"Saved London boroughs to {OUTPUT_CSV}")
