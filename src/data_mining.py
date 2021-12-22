import matplotlib.pyplot as plt

import db
from MySQLutils import connectDB, closeDB

VIEW_NAME = 'SearchView'
ATTRIBUTES = [
    'suspect_age_range',
    'suspect_gender',
    'suspect_ethnicity',
    'legislation',
    'outcome',
    'object',
    'object_caused_outcome',
    'clothing_removal',
]

def filterAttributes(data, attr, one_dim=False):
    attribute_indices = [ATTRIBUTES.index(a) for a in attr]
    filtered_data = [
        tuple([
            col for i, col in enumerate(row)
            if i in attribute_indices
        ])
        for row in data
    ]

    if one_dim == True:
        if len(attr) > 1:
            raise ValueError('attr must have only one value if one_dim is True')

    return filtered_data

if __name__ == '__main__':
    connection, cursor = connectDB()

    query = db.select(VIEW_NAME, attributes=ATTRIBUTES)
    cursor.execute(query)
    search_data = cursor.fetchall()

    outcomes = filterAttributes(search_data, ['outcome'], one_dim=True)
    print(set(outcomes))
    print('')

    ethnicities = filterAttributes(search_data, ['suspect_ethnicity'], one_dim=True)
    print(set(ethnicities))
    print('')

    closeDB(connection, cursor)