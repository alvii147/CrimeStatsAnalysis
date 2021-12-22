import os
import sys
import unittest
import warnings
from unittest.mock import patch
from io import StringIO

import crime
import db

SAMPLE_PERSON = {
    'first_name': 'Paul',
    'last_name': 'Ward',
    'age_range': '55',
    'gender': 'His Greatness',
    'ethnicity': 'White',
    'phone_number': '(519) 888-4567',
    'updated_gender': 'Lord of ECE',
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

SAMPLE_CRIME = {
    'victim_id': '1',
    'code': '110',
    'organization': 'IUCR',
    'location_id': '1',
    'occurrence_date': '2001-09-11',
    'last_updated': '2001-09-11',
    'status': 'Arrested',
    'police_department': 'Chicago Police Department',
    'type': 'Theft',
    'weapon': 'Mjolnir',
    'domestic': '0',
    'description': 'Perpetrator robbed Thors hammer',
}
CRIME_TEST_INPUT = [
    'yes',
    SAMPLE_CRIME['victim_id'],
    'yes',
    SAMPLE_CRIME['code'],
    SAMPLE_CRIME['organization'],
    'yes',
    SAMPLE_CRIME['location_id'],
    SAMPLE_CRIME['occurrence_date'],
    SAMPLE_CRIME['last_updated'],
    SAMPLE_CRIME['status'],
    SAMPLE_CRIME['police_department'],
    SAMPLE_CRIME['type'],
    SAMPLE_CRIME['weapon'],
    SAMPLE_CRIME['domestic'],
    SAMPLE_CRIME['description'],
]

class TestCLI(unittest.TestCase):
    @patch('builtins.input', side_effect=CRIME_TEST_INPUT)
    def test_add_delete_crime(self, magic_mock_obj):
        # add crime
        exit_status = crime.add(['crime'])
        self.assertTrue(exit_status == crime.SUCCESS)
        crime.connection.commit()

        crime_id = crime.cursor.lastrowid
        with patch('sys.stdout', new=StringIO) as fake_out:
            exit_status = crime.show(['crime', str(crime_id)])
            std_out = fake_out.getvalue()

        print(std_out)

    @patch('builtins.input', side_effect=PERSON_TEST_INPUT)
    def test_add_delete_person(self, magic_mock_obj):
        # add person
        exit_status = crime.add(['person'])
        self.assertTrue(exit_status == crime.SUCCESS)
        crime.connection.commit()

        person_id = crime.cursor.lastrowid
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

        # update person
        exit_status = crime.update(['person', str(person_id)])
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

        # delete person
        exit_status = crime.delete(['person', str(person_id)])
        self.assertTrue(exit_status == crime.SUCCESS)

        crime.connection.commit()

        crime.cursor.execute(query)
        output = crime.cursor.fetchall()
        self.assertTrue(len(output) == 0)

    @patch('builtins.input', side_effect=[1, 1])
    def test_background_check(self, magic_mock_obj):
        exit_status = crime.background(['id'])
        self.assertTrue(exit_status == crime.SUCCESS)

if __name__ == '__main__':
    unittest.main(verbosity=2)