import csv
import matplotlib.pyplot as plt
from collections import Counter

STOP_AND_SEARCH_DATA_FILE = '../datasets/london-police-records/london-stop-and-search.csv'
ATTRIBUTES = [
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

def read_csv(filename, ignore=1):
    datafile = csv.reader(open(filename))

    data = []
    for row in datafile:
        if ignore > 0:
            ignore -= 1
            continue

        data.append(row)

    return data

def filterAttributes(data, attr, one_dim=False):
    attribute_indices = [ATTRIBUTES.index(a) for a in attr]
    filtered_data = [
        [
            col for i, col in enumerate(row)
            if i in attribute_indices
        ]
        for row in data
    ]

    if one_dim == True:
        if len(attr) > 1:
            raise ValueError('attr must have only one value if one_dim is True')

        filtered_data = [row[0] for row in filtered_data]

    return filtered_data

if __name__ == '__main__':
    search_data = read_csv(STOP_AND_SEARCH_DATA_FILE)

    outcome_idx = ATTRIBUTES.index('outcome')
    ethnicity_idx = ATTRIBUTES.index('detailed_ethnicity')
    gender_idx = ATTRIBUTES.index('gender')

    filter_func = lambda row: len(row[outcome_idx].strip()) > 0 and len(row[ethnicity_idx].strip()) > 0 and len(row[gender_idx].strip()) > 0
    search_data = list(filter(filter_func, search_data))

    outcomes = filterAttributes(search_data, ['outcome'], one_dim=True)

    ethnicities = filterAttributes(search_data, ['detailed_ethnicity'], one_dim=True)
    ethnicities = [e.split('(')[1] for e in ethnicities]
    ethnicities = [e.split(')')[0] for e in ethnicities]

    genders = filterAttributes(search_data, ['gender'], one_dim=True)
    genders = [g[0] for g in genders]

    iter_range = min(len(outcomes), len(ethnicities), len(genders))
    data = [[ethnicities[i], genders[i], outcomes[i]] for i in range(iter_range)]

    outcome_types = sorted(list(set(outcomes)))

    ethnicity_labels = ['A1', 'A2', 'A3', 'A9', 'B1', 'B2', 'B9', 'W1', 'W2', 'W9']
    gender_labels = ['M', 'F', 'O']

    ethnicity_counter = Counter(ethnicities)
    gender_counter = Counter(genders)

    eth_colors = ["#509f87", "#b4ddd4", "#6ceac0", "#a8e667", "#a96370", "#efbba2", "#245a62", "#509f87", "#a93705"]
    ge_colors = ["#68affc", "#bc6b85", "#c0e087", "#fb4e93", "#18519b", "#ca5100", "#06a56c", "#6c36a3"]

    ethnicity_outcomes = {}
    gender_outcomes = {}
    for oc in outcome_types:
        filtered_data = [row[0 : 2] for row in data if row[2] == oc]
        ec = Counter([row[0] for row in filtered_data])
        gc = Counter([row[1] for row in filtered_data])
        ethnicity_outcomes[oc] = [(ec.get(label, 0) * 100) / ethnicity_counter.get(label) for label in ethnicity_labels]
        gender_outcomes[oc] = [(gc.get(label, 0) * 100) / gender_counter.get(label) for label in gender_labels]

    fig, ax = plt.subplots()

    bottom = [0] * len(ethnicity_labels)
    for i, oc in enumerate(outcome_types):
        ax.bar(ethnicity_labels, ethnicity_outcomes[oc], 0.35, bottom=bottom, label=oc, color=eth_colors[i])
        for i in range(len(ethnicity_labels)):
            bottom[i] += ethnicity_outcomes[oc][i]

    ax.set_ylabel('Percentage')
    ax.set_xlabel('Ethnicity')
    ax.set_title('Stop-&-Search Outcomes by Ethnicity')
    ax.legend()

    plt.show()

    fig, ax = plt.subplots()

    bottom = [0] * len(gender_labels)
    for i, oc in enumerate(outcome_types):
        ax.bar(gender_labels, gender_outcomes[oc], 0.15, bottom=bottom, label=oc, color=ge_colors[i])
        for i in range(len(gender_labels)):
            bottom[i] += gender_outcomes[oc][i]

    ax.set_ylabel('Percentage')
    ax.set_xlabel('Gender')
    ax.set_title('Stop-&-Search Outcomes by Gender')
    ax.legend()

    plt.show()