import unittest
import warnings
from unittest.mock import patch
from io import StringIO

import crime
import db
import utils

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

SAMPLE_COMPLAINT = {
    'code': '110',
    'organization': 'IUCR',
    'location_id': '1',
    'occurrence_date': '2015-09-06',
    'last_updated': '2015-09-06',
    'status': 'Filed',
    'police_department': 'Chicago Police Department',
    'type': 'Robbery',
    'reported_date': '2015-09-06',
    'description': 'My house got robbed',
}

COMPLAINT_TEST_INPUT = [
    'yes',
    SAMPLE_COMPLAINT['code'],
    SAMPLE_COMPLAINT['organization'],
    'yes',
    SAMPLE_COMPLAINT['location_id'],
    SAMPLE_COMPLAINT['occurrence_date'],
    SAMPLE_COMPLAINT['last_updated'],
    SAMPLE_COMPLAINT['status'],
    SAMPLE_COMPLAINT['police_department'],
    SAMPLE_COMPLAINT['type'],
    SAMPLE_COMPLAINT['reported_date'],
    SAMPLE_COMPLAINT['description'],
    'no',
    'yes',
    'yes',
    '110',
    'no',
    'no',
]

def isAttributeLine(l):
    for w in l:
        for c in w:
            if c != '-':
                return True

    return False

def parseShowOutput(output):
    output = [o.strip() for o in output.split('\n') if len(o.strip()) > 1]
    output = [[p.strip() for p in o.split('|')] for o in output]
    output = [[p for p in o if len(p) > 0] for o in output]
    output = list(filter(isAttributeLine, output))

    return output

class TestCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # clean db
        crime.clean('DUMMY')
        # create tables
        crime.create('DUMMY')
        # load tables
        crime.load('DUMMY')

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
        show_output = parseShowOutput(show_output)
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

    @patch('builtins.input', side_effect=COMPLAINT_TEST_INPUT)
    def test_add_filter_complaint(self, magic_mock_obj):
        # add complaint
        exit_status = crime.add(['complaint'])
        self.assertTrue(exit_status == crime.SUCCESS)
        crime.connection.commit()

        # filter complaint by code
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exit_status = crime.filter(['complaint'])
            show_output = fake_out.getvalue()

        self.assertTrue(exit_status == crime.SUCCESS)
        show_output = parseShowOutput(show_output)
        self.assertTrue(len(show_output) > 1)
        self.assertTrue(show_output[-1][3] == SAMPLE_COMPLAINT['code'])

    @patch('builtins.input', side_effect=PERSON_TEST_INPUT)
    def test_add_show_delete_person(self, magic_mock_obj):
        # add person
        exit_status = crime.add(['person'])
        self.assertTrue(exit_status == crime.SUCCESS)
        crime.connection.commit()

        person_id = crime.cursor.lastrowid
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exit_status = crime.show(['person', str(person_id)])
            show_output = fake_out.getvalue()

        self.assertTrue(exit_status == crime.SUCCESS)
        show_output = parseShowOutput(show_output)
        self.assertTrue(len(show_output) > 0)

        self.assertTrue(show_output[-1][1] == SAMPLE_PERSON['first_name'])
        self.assertTrue(show_output[-1][2] == SAMPLE_PERSON['last_name'])
        self.assertTrue(show_output[-1][3] == SAMPLE_PERSON['age_range'])
        self.assertTrue(show_output[-1][4] == SAMPLE_PERSON['gender'])
        self.assertTrue(show_output[-1][5] == SAMPLE_PERSON['ethnicity'])
        self.assertTrue(show_output[-1][6] == SAMPLE_PERSON['phone_number'])

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

class TestUtils(unittest.TestCase):
    def test_isNull(self):
        self.assertTrue(utils.isNull('\'NULL\''))
        self.assertTrue(utils.isNull('"NULL"'))
        self.assertFalse(utils.isNull('NULL'))
        self.assertFalse(utils.isNull('porcupine'))

    def test_isQuoted(self):
        self.assertTrue(utils.isQuoted('\'Is today tomorrow New Zealand?\''))
        self.assertTrue(utils.isQuoted('"Is baby powder made out of babies?"', quote='"'))
        self.assertFalse(utils.isQuoted('Electric outlets look surprised why?'))

    def test_stripQuotes(self):
        s = 'Foot same length Europe?'
        self.assertTrue(utils.stripQuotes(f'\'{s}\'', quote='\'') == s)
        self.assertTrue(utils.stripQuotes(f'"{s}"', quote='"') == s)
        self.assertFalse(utils.stripQuotes(f'\'{s}\'', quote='"') == s)
        self.assertFalse(utils.stripQuotes(f'"{s}"', quote='\'') == s)
        self.assertTrue(utils.stripQuotes(f'\'{s}') != s)
        self.assertTrue(utils.stripQuotes(s) == s)

if __name__ == '__main__':
    unittest.main(verbosity=2)