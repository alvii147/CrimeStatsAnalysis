import csv
from collections import Counter
import matplotlib.pyplot as plt

SEARCH_DATA_FILE = '../../datasets/london-police-records/london-stop-and-search.csv'
SEARCH_DATA_ATTRIBUTES = [
    'type',
    'occurrence_date',
    'part_of_policing_operation',
    'policing_operation',
    'latitude',
    'longitude',
    'gender',
    'age_range',
    'detailed_ethnicity',
    'ethnicity',
    'legislation',
    'object',
    'outcome',
    'object_caused_outcome',
    'clothing_removal',
]

COLORS = [
    "#509f87",
    "#b4ddd4",
    "#6ceac0",
    "#a8e667",
    "#a96370",
    "#efbba2",
    "#245a62",
    "#509f87",
    "#a93705"
]

def read_csv(filename, ignore=1):
    datafile = csv.reader(open(filename))

    data = []
    for row in datafile:
        if ignore > 0:
            ignore -= 1
            continue

        data.append(row)

    return data

def isRowEmpty(row):
    for val in row:
        if isinstance(val, str) and len(val.strip()) == 0:
            return True

    return False

def filterOutEmptyRows(data):
    filtered_data = [
        row for row in data
        if not isRowEmpty(row)
    ]

    return filtered_data

def filterAttributes(data, col_indices, one_dim=False):
    filtered_data = [
        [
            col for i, col in enumerate(row)
            if i in col_indices
        ]
        for row in data
    ]

    if one_dim == True:
        if len(col_indices) > 1:
            raise ValueError('attr must have only one value if one_dim is True')

        filtered_data = [row[0] for row in filtered_data]

    return filtered_data

def getAttrCountByOutcome(data, attr_labels):
    outcome_types = sorted(list(set(
        [row[1] for row in data]
    )))

    attr_total_counter = Counter([row[0] for row in data])

    attr_outcomes_counter = {}
    for ot in outcome_types:
        filt_data = [row[0] for row in data if row[1] == ot]
        attr_counter = Counter([row for row in filt_data])
        attr_outcomes_counter[ot] = [
            (attr_counter.get(label, 0) * 100) / attr_total_counter[label]
            for label in attr_labels
        ]

    return attr_outcomes_counter

def plotOutcomeBarGraph(attr_outcomes_counter, labels, width=0.3, xlabel='Attribute Values', ylabel='Percentage', title='Stop-&-Search Outcomes by Attribute', colors=COLORS):
    fig, ax = plt.subplots()

    bottom = [0] * len(labels)
    for i, item in enumerate(sorted(attr_outcomes_counter.items())):
        k = item[0]
        v = item[1]
        ax.bar(labels, v, width, bottom=bottom, label=k, color=colors[i])

        for j in range(len(labels)):
            bottom[j] += v[j]

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    plt.show()