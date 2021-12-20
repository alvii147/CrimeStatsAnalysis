# This script is used for demonstration purposes only.
# It is used to generate random names and phone numbers for people in the database

import random

def read_lines(path):
    file = open(path, "r")
    data = file.read().split('\n')[:-1]
    file.close()
    return data

MALE = read_lines("people/male.txt")
FEMALE = read_lines("people/female.txt")
OTHER = read_lines("people/other.txt")
LAST = read_lines("people/last.txt")
PHONE = read_lines("people/phone.txt")

COUNT = 5000
NULL = False   # Set to True to return NULL for names and phone numbers

assert len(MALE) == COUNT
assert len(FEMALE) == COUNT
assert len(OTHER) == COUNT
assert len(LAST) == COUNT
assert len(PHONE) == COUNT

def random_index():
    return random.randint(0, COUNT - 1)

def first_name(gender = "Other"):
    if NULL:
        return 'NULL'
    elif gender == "Male":
        return MALE[random_index()]
    elif gender == "Female":
        return FEMALE[random_index()]
    else:
        return OTHER[random_index()]

def last_name():
    if NULL:
        return 'NULL'
    else:
        return LAST[random_index()]

def phone_number():
    if NULL:
        return 'NULL'
    else:
        return PHONE[random_index()]

def info(gender = "Other"):
    return first_name(gender), last_name(), phone_number()
