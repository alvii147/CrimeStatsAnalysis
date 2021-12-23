import utils

if __name__ == '__main__':
    search_data = utils.read_csv(utils.SEARCH_DATA_FILE)
    outcome_idx = utils.SEARCH_DATA_ATTRIBUTES.index('outcome')

    # ---------------------------------------------------------------------
    # AGE RANGE
    # ---------------------------------------------------------------------

    age_range_idx = utils.SEARCH_DATA_ATTRIBUTES.index('age_range')
    age_range_outcomes = utils.filterAttributes(
        search_data,
        [age_range_idx, outcome_idx],
    )
    age_range_outcomes = utils.filterOutEmptyRows(age_range_outcomes)

    age_range_labels = ['under 10', '10-17', '18-24', '25-34', 'over 34']
    age_range_by_outcomes = utils.getAttrCountByOutcome(age_range_outcomes, age_range_labels)
    utils.plotOutcomeBarGraph(
        age_range_by_outcomes,
        age_range_labels,
        xlabel='Age Range',
        title='Stop-&-Search Outcomes by Age Range',
    )

    # ---------------------------------------------------------------------
    # OBJECT
    # ---------------------------------------------------------------------

    object_idx = utils.SEARCH_DATA_ATTRIBUTES.index('object')
    object_outcomes = utils.filterAttributes(
        search_data,
        [object_idx, outcome_idx],
    )
    object_outcomes = utils.filterOutEmptyRows(object_outcomes)

    object_labels = ['Controlled drugs', 'Article for use in theft', 'Fireworks', 'Articles for use in criminal damage', 'Firearms', 'Stolen goods', 'Evidence of offences under the Act', 'Anything to threaten or harm anyone', 'Offensive weapons']
    object_wrapped_labels = ['Controlled\ndrugs', 'Article for use\nin theft', 'Fireworks', 'Articles for use\nin criminal damage', 'Firearms', 'Stolen goods', 'Evidence of\noffences\nunder the Act', 'Anything to\nthreaten or\nharm anyone', 'Offensive\nweapons']
    object_by_outcome = utils.getAttrCountByOutcome(object_outcomes, object_labels)
    utils.plotOutcomeBarGraph(
        object_by_outcome,
        object_wrapped_labels,
        xlabel='Object',
        title='Stop-&-Search Outcomes by Searched Object',
    )

    # ---------------------------------------------------------------------
    # GENDER
    # ---------------------------------------------------------------------

    gender_idx = utils.SEARCH_DATA_ATTRIBUTES.index('gender')
    gender_outcomes = utils.filterAttributes(
        search_data,
        [gender_idx, outcome_idx],
    )
    gender_outcomes = utils.filterOutEmptyRows(gender_outcomes)
    gender_outcomes = [[row[0][0], row[1]] for row in gender_outcomes]

    gender_labels = ['M', 'F', 'O']
    gender_by_outcome = utils.getAttrCountByOutcome(gender_outcomes, gender_labels)
    utils.plotOutcomeBarGraph(
        gender_by_outcome,
        gender_labels,
        xlabel='Gender',
        title='Stop-&-Search Outcomes by Searched Gender',
    )

    # ---------------------------------------------------------------------
    # LEGISLATION
    # ---------------------------------------------------------------------

    legislation_idx = utils.SEARCH_DATA_ATTRIBUTES.index('legislation')
    legislation_outcomes = utils.filterAttributes(
        search_data,
        [legislation_idx, outcome_idx],
    )
    legislation_outcomes = utils.filterOutEmptyRows(legislation_outcomes)

    legislation_labels = ['Criminal Justice and Public Order Act 1994 (section 60)', 'Misuse of Drugs Act 1971 (section 23)', 'Police and Criminal Evidence Act 1984 (section 1)', 'Criminal Justice Act 1988 (section 139B)', 'Firearms Act 1968 (section 47)']
    legislation_wrapped_labels = ['Criminal Justice\nand Public\nOrder Act 1994\n(section 60)', 'Misuse of Drugs\nAct 1971\n(section 23)', 'Police and\nCriminal Evidence\nAct 1984\n(section 1)', 'Criminal Justice\nAct 1988\n(section 139B)', 'Firearms Act\n1968\n(section 47)']
    legislation_by_outcome = utils.getAttrCountByOutcome(legislation_outcomes, legislation_labels)
    utils.plotOutcomeBarGraph(
        legislation_by_outcome,
        legislation_wrapped_labels,
        xlabel='Legislation',
        title='Stop-&-Search Outcomes by Legislation',
    )

    # ---------------------------------------------------------------------
    # DETAILED ETHNICITY
    # ---------------------------------------------------------------------

    detailed_ethnicity_idx = utils.SEARCH_DATA_ATTRIBUTES.index('detailed_ethnicity')
    detailed_ethnicity_outcomes = utils.filterAttributes(
        search_data,
        [detailed_ethnicity_idx, outcome_idx],
    )
    detailed_ethnicity_outcomes = utils.filterOutEmptyRows(detailed_ethnicity_outcomes)
    detailed_ethnicity_outcomes = [[row[0].split('(')[1], row[1]] for row in detailed_ethnicity_outcomes]
    detailed_ethnicity_outcomes = [[row[0].split(')')[0], row[1]] for row in detailed_ethnicity_outcomes]

    detailed_ethnicity_labels = ['A1', 'A2', 'A3', 'A9', 'B1', 'B2', 'B9', 'W1', 'W2', 'W9']
    detailed_ethnicity_by_outcome = utils.getAttrCountByOutcome(detailed_ethnicity_outcomes, detailed_ethnicity_labels)
    utils.plotOutcomeBarGraph(
        detailed_ethnicity_by_outcome,
        detailed_ethnicity_labels,
        xlabel='Detailed Ethnicity',
        title='Stop-&-Search Outcomes by Detailed Ethnicity',
    )