import os
import sys
import unittest
import warnings
from unittest.mock import patch

import crime
import db

SAMPLE_PERSON = {
    'first_name': 'Paul',
    'last_name': 'Ward',
    'age_range': '55',
    'gender': 'His Greatness',
    'ethnicity': 'White',
    'phone_number': '(519) 888-4567',
    'updated_gender' : 'Lord of ECE',
}

PERSON_TEST_INPUT = [
    SAMPLE_PERSON['first_name'],
    SAMPLE_PERSON['last_name'],
    SAMPLE_PERSON['age_range'],
    SAMPLE_PERSON['gender'],
    SAMPLE_PERSON['ethnicity'],
    SAMPLE_PERSON['phone_number'],
    'no',
    'no',
    'no',
    'yes',
    SAMPLE_PERSON['updated_gender'],
    'no',
    'no',
]

crime_test_data = [
    'yes',
]

def disable_stdout():
    sys.stdout = open(os.devnull, 'w')

def enable_stdout():
    sys.stdout = sys.__stdout__

class TestCLI(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)

    @patch('builtins.input', side_effect=SAMPLE_PERSON)
    def test_add_delete_person(self, magic_mock_obj):
        # add person
        print('\n\nAdding person ...')
        for k, v in SAMPLE_PERSON.items():
            print('  ', k, ':', v)

        disable_stdout()
        exit_status = crime.add(['person'])
        enable_stdout()

        self.assertTrue(exit_status == crime.SUCCESS)

        person_id = crime.cursor.lastrowid
        crime.connection.commit()

        where = f'person_id={person_id}'
        query = db.select('Person', where=where)

        crime.cursor.execute(query)
        output = crime.cursor.fetchall()

        self.assertTrue(len(output) > 0)
        self.assertTrue(output[0][1] == SAMPLE_PERSON['first_name'])
        self.assertTrue(output[0][2] == SAMPLE_PERSON['last_name'])
        self.assertTrue(output[0][3] == SAMPLE_PERSON['age_range'])
        self.assertTrue(output[0][4] == SAMPLE_PERSON['gender'])
        self.assertTrue(output[0][5] == SAMPLE_PERSON['ethnicity'])
        self.assertTrue(output[0][6] == SAMPLE_PERSON['phone_number'])

        print('Add operation successful')

        # update person
        print(
            '\nUpdating gender from',
            SAMPLE_PERSON['gender'],
            'to',
            SAMPLE_PERSON['updated_gender'],
            '...',
        )

        disable_stdout()
        exit_status = crime.update(['person', str(person_id)])
        enable_stdout()

        self.assertTrue(exit_status == crime.SUCCESS)

        crime.cursor.execute(query)
        output = crime.cursor.fetchall()

        self.assertTrue(len(output) > 0)
        self.assertTrue(output[0][1] == SAMPLE_PERSON['first_name'])
        self.assertTrue(output[0][2] == SAMPLE_PERSON['last_name'])
        self.assertTrue(output[0][3] == SAMPLE_PERSON['age_range'])
        self.assertTrue(output[0][4] == SAMPLE_PERSON['updated_gender'])
        self.assertTrue(output[0][5] == SAMPLE_PERSON['ethnicity'])
        self.assertTrue(output[0][6] == SAMPLE_PERSON['phone_number'])

        print('Update operation successful')

        # delete person
        print('\nDeleting person ...')

        disable_stdout()
        exit_status = crime.delete(['person', str(person_id)])
        enable_stdout()

        self.assertTrue(exit_status == crime.SUCCESS)

        crime.connection.commit()

        crime.cursor.execute(query)
        output = crime.cursor.fetchall()

        self.assertTrue(len(output) == 0)

        print('Delete operation successful')

    @patch('builtins.input', side_effect=[1, 1])
    def test_background_check(self, magic_mock_obj):
        print('\n\nRunning background check ...')

        disable_stdout()
        exit_status = crime.background(['id'])
        enable_stdout()

        self.assertTrue(exit_status == crime.SUCCESS)

        print('Background check successfull')

if __name__ == '__main__':
    unittest.main(verbosity=2)