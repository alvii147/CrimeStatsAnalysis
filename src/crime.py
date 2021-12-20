import log
import os
import utils
import transfer
import db

from sys import argv
from MySQLutils import connectDB, closeDB
from utils import consoleFriendly

argc = len(argv)

INTERPRETER = "python3"
PROGRAM = os.path.basename(argv[0])
TABLES = utils.readJSON("tables.json")
SUCCESS = 0
ERROR = -1

connection = None
cursor = None

# ===================== COMMANDS ===================== #

# --------------------- CREATION --------------------- #

def create():
    utils.runQueries("SQL/create.sql")
    utils.runQueries("SQL/keys.sql")

def load():
    log.note("Add arg for number of lines to load from each CSV")
    utils.runQueries("SQL/create_temp.sql")
    utils.runQueries("SQL/load.sql")
    transfer.transfer_all()
    utils.runQueries("SQL/drop.sql")

def clean():
    utils.runQueries("SQL/clean.sql")

def clear():
    utils.runQueries("SQL/clear.sql")

# --------------------- ADD --------------------- #

def add_codes():
    pass

def prompt_attributes(table, ignore = []):
    record = {}
    for attribute in TABLES[table]:
        if attribute in ignore:
            continue
        value = input(f"{attribute}: ")
        if value == "":
            value = 'NULL'
        record[attribute] = value
    return record

def insert_person(person):
    query = db.insert(
        "Person",
        first_name = person["first_name"],
        last_name = person["last_name"],
        phone_number = person["phone_number"],
        age_range = person["age_range"],
        gender = person["gender"],
        ethnicity = person["ethnicity"]
    )

    try:
        cursor.execute(query)
        log.info(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to insert into table Person:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None

    person_id = cursor.lastrowid
    return person_id

def insert_location(location):
    query = db.insert(
        "Location",
        latitude = location["latitude"],
        longitude = location["longitude"],
        premises = location["premises"],
        area = location["area"],
        precinct = location["precinct"],
        ward = location["ward"],
        borough = location["borough"],
        city = location["city"],
        state = location["state"],
        country = location["country"]
    )

    try:
        cursor.execute(query)
        log.info(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to insert into table Location:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None

    location_id = cursor.lastrowid
    return location_id

def insert_incident(incident):
    query = db.insert(
        "Incident",
        location_id = incident["location_id"],
        occurrence_date = incident["occurrence_date"],
        police_department = incident["police_department"],
        type = incident["type"],
        status = incident["status"],
        last_updated = incident["last_updated"]
    )

    try:
        cursor.execute(query)
        log.info(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to insert into table incident:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None

    incident_id = cursor.lastrowid
    return incident_id

def insert_complaint(complaint):
    query = db.insert(
       "Complaint",
       incident_id = complaint["incident_id"],
       code = complaint["code"],
       organization = complaint["organization"],
       reported_date = complaint["reported_date"],
       description = complaint["description"]
    )

    try:
        cursor.execute(query)
        log.info(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to insert into table Compliant:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None

    complaint_id = cursor.lastrowid
    return complaint_id

def insert_crime(crime):
    query = db.insert(
        "Crime",
        incident_id = crime["incident_id"],
        code = crime["code"],
        organization = crime["organization"],
        victim_id = crime["victim_id"],
        weapon = crime["weapon"],
        description = crime["description"],
        domestic = crime["domestic"]
    )

    try:
        cursor.execute(query)
        log.info(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to insert into table Crime:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None

    crime_id = cursor.lastrowid
    return crime_id

def insert_search(search):
    query = db.insert(
        "Search",
        incident_id = search["incident_id"],
        suspect_id = search["suspect_id"],
        legislation = search["legislation"],
        object = search["object"],
        outcome = search["outcome"],
        object_caused_outcome = search["object_caused_outcome"],
        clothing_removal = search["clothing_removal"]
    )

    try:
        cursor.execute(query)
        log.info(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to insert into table Search:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None

    search_id = cursor.lastrowid
    return search_id

def add_incident():
    log.info(f"Choose one of the following options: ")
    log.info(f"1. Complaint : Incidents reported to police")
    log.info(f"2. Crimes    : Crimes that have actually taken place")
    log.info(f"3. Search    : A suspect was detained and searched")

    choice = ''
    CHOICES = ['1', '2', '3']
    while choice not in CHOICES:
        choice = input("[1-3]: ")

    log.info("Press [Enter] to skip unknown information (NULL)")

    log.info("Location:")
    location = prompt_attributes('Location', ignore = ['location_id'])
    location_id = insert_location(location)

    if location_id is None:
        log.error("Failed to insert location")
        return ERROR

    log.info("Incident:")
    incident = prompt_attributes('Incident', ignore = ['location_id', 'incident_id'])
    incident['location_id'] = location_id
    incident_id = insert_incident(incident)

    if incident_id is None:
        log.error("Failed to insert incident")
        return ERROR

    if choice == '1':
        log.info("Complaint:")
        complaint = prompt_attributes('Complaint', ignore = ['complaint_id', 'incident_id'])
        complaint['incident_id'] = incident_id

        complaint_id = insert_complaint(complaint)
        if complaint_id is None:
            log.error("Failed to insert complaint")
            return ERROR

        log.success(f"Added complaint incident '{complaint_id}' to database")

    elif choice == '2':
        log.info("Victim:")
        victim = prompt_attributes('Person', ignore = ['person_id'])
        victim_id = insert_person(victim)

        if victim_id is None:
            log.error("Failed to insert victim")
            return ERROR

        log.info("Crime:")
        crime = prompt_attributes('Crime', ignore = ['crime_id', 'incident_id', 'victim_id'])
        crime['victim_id'] = victim_id
        crime['incident_id'] = incident_id

        crime_id = insert_crime(crime)
        if crime_id is None:
            log.error("Failed to insert crime")
            return ERROR

        log.success(f"Added crime incident '{crime_id}' to database")

    elif choice == '3':
        log.info("Suspect:")
        suspect = prompt_attributes('Person', ignore = ['person_id'])
        suspect_id = insert_person(suspect)

        if suspect_id is None:
            log.error("Failed to insert suspect")
            return ERROR

        log.info("Search:")
        search = prompt_attributes('Search', ignore = ['search_id', 'incident_id', 'suspect_id'])
        search['suspect_id'] = suspect_id
        search['incident_id'] = incident_id

        search_id = insert_search(search)
        if search_id is None:
            log.error("Failed to insert search")
            return ERROR

        log.success(f"Added search incident '{search_id}' to database")

    return SUCCESS

def add_location():
    pass

ADD_HELP = {
    "codes":    "Add new crime codes from a crime enforcement organization",
    "incident": "Add a new crime, complaint, or search",
    "location": "Add a new location",
}

ADD_COMMANDS = {
    "codes":    add_codes,
    "incident": add_incident,
    "location": add_location,
}

def help_add():
    log.info(f"{INTERPRETER} {PROGRAM} add code     : {ADD_HELP['codes']}")
    log.info(f"{INTERPRETER} {PROGRAM} add incident : {ADD_HELP['incident']}")
    log.info(f"{INTERPRETER} {PROGRAM} add location : {ADD_HELP['location']}")

ADD_MIN_ARGC = 2
ADD_MAX_ARGC = 3

def add():
    if argc < ADD_MIN_ARGC or argc > ADD_MAX_ARGC:
        log.error(f"Incorrect number of arguments")
        help_add()
        return ERROR

    if argc == ADD_MIN_ARGC:
        help_add()
        return SUCCESS

    command = argv[2]

    if command not in ADD_COMMANDS:
        log.error(f"Unknown command '{command}'")
        log.info(f"Try '{INTERPRETER} {PROGRAM} add'")
        return ERROR

    return ADD_COMMANDS[command]()

# --------------------- HELP --------------------- #

HELP = {
    "help":   "Show this message",
    "create": "Create all tables",
    "load":   "Load data from CSVs into tables",
    "clear":  "Delete all entries in tables",
    "clean":  "Drop all tables from database",
    "add":    "Add entries to the database",
}

def help():
    log.info("--------------------------------------------------------------")
    log.info(f"Usage: {INTERPRETER} {PROGRAM} <command> [arguments]")
    log.info("--------------------------------------------------------------")

    log.info(f"{INTERPRETER} {PROGRAM} help   : {HELP['help']}")
    log.info(f"{INTERPRETER} {PROGRAM} create : {HELP['create']}")
    log.info(f"{INTERPRETER} {PROGRAM} load   : {HELP['load']}")
    log.info(f"{INTERPRETER} {PROGRAM} clear  : {HELP['clear']}")
    log.info(f"{INTERPRETER} {PROGRAM} clean  : {HELP['clean']}")
    log.info(f"{INTERPRETER} {PROGRAM} add    : {HELP['add']}")

    log.info("--------------------------------------------------------------")

    log.note("TODO:")
    log.note("finish add location ")
    log.note("Remove nulls from database by adding default values ex last_updated")
    log.note("add in the modify query statements ")
    log.note("add in the show statements for querying ")
    log.note("add in delete ")
    log.note("add in indexes into the database ")
    log.note("finish the report ")
    log.note("create presentation ")
    log.note("create the video ")
    log.note("update ER model ")

    log.note("add in the extra attributes into the database to hit 50 (maybe) ")
    log.note("Do a datamine ")

    return SUCCESS

# ===================== MAIN ===================== #

COMMANDS = {
    "help":   help,
    "create": create,
    "load":   load,
    "clean":  clean,
    "clear":  clear,
    "add":    add,
}

MIN_ARGC = 1
MAX_ARGC = 3


def usage():
    log.info(f"Usage: {INTERPRETER} {PROGRAM} <command> [arguments]")
    log.info(f"Try '{INTERPRETER} {PROGRAM} help'")
    return SUCCESS

if argc < MIN_ARGC or argc > MAX_ARGC:
    log.error("Incorrect number of arguments")
    usage()
    exit(ERROR)

if argc == 1:
    command = "help"
else:
    command = argv[1]

if command not in COMMANDS:
    log.error(f"Unknown command '{command}'")
    usage()
    exit(ERROR)

connection, cursor = connectDB()
result = COMMANDS[command]()

if result == SUCCESS:
    connection.commit()

closeDB(connection, cursor)
exit(result)
