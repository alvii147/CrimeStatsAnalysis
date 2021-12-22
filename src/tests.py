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

def isAttributeLine(l):
    for w in l:
        for c in w:
            if c != '-':
                return True

    return False

class TestCLI(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

    @patch('builtins.input', side_effect=CRIME_TEST_INPUT)
    def test_add_show_delete_crime(self, magic_mock_obj):
        # add crime
        exit_status = crime.add(['crime'])
        self.assertTrue(exit_status == crime.SUCCESS)
        crime.connection.commit()

        # show crime
        crime_id = crime.cursor.lastrowid
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exit_status = crime.show(['crime', str(crime_id)])
            show_output = fake_out.getvalue()

        self.assertTrue(exit_status == crime.SUCCESS)

        show_output = [o.strip() for o in show_output.split('\n') if len(o.strip()) > 1]
        show_output = [[p.strip() for p in o.split('|')] for o in show_output]
        show_output = [[p for p in o if len(p) > 0] for o in show_output]
        show_output = list(filter(isAttributeLine, show_output))
        self.assertTrue(len(show_output) > 1)

        attr = show_output[-1]
        print(attr)
        self.assertTrue(attr[2] == SAMPLE_CRIME['code'])
        self.assertTrue(attr[3] == SAMPLE_CRIME['organization'])
        self.assertTrue(attr[5] == SAMPLE_CRIME['weapon'])
        self.assertTrue(attr[6] == SAMPLE_CRIME['domestic'])
        self.assertTrue(attr[7] == SAMPLE_CRIME['description'])

        # delete crime
        exit_status = crime.delete(['crime', str(crime_id)])
        self.assertTrue(exit_status == crime.SUCCESS)
        crime.connection.commit()

        where = f'crime_id={crime_id}'
        query = db.select('Crime', where=where)
        crime.cursor.execute(query)
        output = crime.cursor.fetchall()
        self.assertTrue(len(output) == 0)

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