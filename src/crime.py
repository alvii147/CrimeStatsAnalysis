import log
import os
import utils
import transfer
import db

from sys import argv

argc = len(argv)

INTERPRETER = "python3"
PROGRAM = os.path.basename(argv[0])
TABLES = utils.readJSON("tables.json")
SUCCESS = 0
ERROR = -1

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

# return person id
def insert_person(person):
    query = db.insert(
        "Person",
        #person_id = person["person_id"],
        first_name = person["first_name"],
        last_name = person["last_name"],
        phone_number = person["phone_number"],
        age_range = person["age_range"],
        gender = person["gender"],
        ethnicity = person["ethnicity"]
    )

    print(query)
    return

# return incident ID
def insert_incident(location, incident):
    #query = db.insert(
    #    'Location',
    #    latitude = location['latitude'],
    #    longitude = location['longitude'],
    #    premises = location['premises'],
    #    area = location['area'],
    #    precinct = location['precinct'],
    #    ward = location['ward'],
    #    borough = location['borough'],
    #    city = location['city'],
    #    state = location['state'],
    #    country = location['country']
    #)
    pass

def insert_complaint(complaint, incident_id):
    pass

def insert_crime(crime, incident_id, victim_id):
    pass

def insert_search(search, incident_id, suspect_id):
    pass

def add_incident():
    #prompt_incident_info()
    # prompt for if its a compliant search or crime
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
    log.info("Incident:")
    incident = prompt_attributes('Incident', ignore = ['location_id', 'incident_id'])

    if choice == '1':
        log.info("Complaint:")
        complaint = prompt_attributes('Complaint', ignore = ['complaint_id', 'incident_id'])
        #query = db.insert('Incident',
        #    "Complaint":
        #    #complaint_id = complaint_id,
        #    #incident_id = incident_id,
        #    code = code,
        #    organization = organization,
        #    reported_date = reported_date,
        #    description = description
    elif choice == '2':
        log.info("Crime:")
        crime = prompt_attributes('Crime', ignore = ['crime_id', 'incident_id', 'victim_id'])
        log.info("Victim:")
        victim = prompt_attributes('Person', ignore = ['person_id'])

        #insert_incident(location, incident)
        insert_person(victim)

        log.note("add person id to crime after getting person id then insert person ID")
    elif choice == '3':
        log.info("Search:")
        search = prompt_attributes('Search', ignore = ['search_id', 'incident_id', 'suspect_id'])
        log.info("Suspect:")
        suspect = prompt_attributes('Person', ignore = ['person_id'])

    log.note("insert location first followed by incident with correct id")

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
    log.info("--------------------------------------------------------------------------------")
    log.info(f"Usage: {INTERPRETER} {PROGRAM} <command> [arguments]")
    log.info("--------------------------------------------------------------------------------")

    log.info(f"{INTERPRETER} {PROGRAM} help   : {HELP['help']}")
    log.info(f"{INTERPRETER} {PROGRAM} create : {HELP['create']}")
    log.info(f"{INTERPRETER} {PROGRAM} load   : {HELP['load']}")
    log.info(f"{INTERPRETER} {PROGRAM} clear  : {HELP['clear']}")
    log.info(f"{INTERPRETER} {PROGRAM} clean  : {HELP['clean']}")
    log.info(f"{INTERPRETER} {PROGRAM} add    : {HELP['add']}")

    log.info("--------------------------------------------------------------------------------")

    return SUCCESS

# ===================== PROGRAM ===================== #

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

exit(COMMANDS[command]())
