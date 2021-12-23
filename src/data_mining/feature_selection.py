import warnings
import math
from scipy import stats

import utils

OMIT_ATTRIBUTES = [
    'type',
    'occurrence_date',
    'part_of_policing_operation',
    'latitude',
    'longitude',
    'outcome',
    'object_caused_outcome',
    'clothing_removal',
]

warnings.filterwarnings('ignore', category=RuntimeWarning)

if __name__ == '__main__':
    search_data = utils.read_csv(utils.SEARCH_DATA_FILE)

    rho, pvalue = stats.spearmanr(search_data, axis=0)

    outcome_idx = utils.SEARCH_DATA_ATTRIBUTES.index('outcome')
    outcome_correlation = [
        [utils.SEARCH_DATA_ATTRIBUTES[i], rho[outcome_idx][i]]
        for i in range(len(utils.SEARCH_DATA_ATTRIBUTES))
    ]

    outcome_correlation = list(filter(
        lambda x: not math.isnan(x[1]) and x[0] not in OMIT_ATTRIBUTES,
        outcome_correlation,
    ))

    outcome_correlation = list(reversed(sorted(
        outcome_correlation,
        key=lambda x: abs(x[1]),
    )))

    print('{:20s} {:20s}'.format('Attribute', 'Correlation'))
    for corr in outcome_correlation:
        print('{:20s} {:20s}'.format(corr[0], str(corr[1])))