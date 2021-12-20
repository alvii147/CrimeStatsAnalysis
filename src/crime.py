import log
import os
import utils
import transfer
import db

from sys import argv
from MySQLutils import connectDB, closeDB
from utils import consoleFriendly, yes, no

argc = len(argv)

INTERPRETER = "python3"
PROGRAM = os.path.basename(argv[0])
TABLES = utils.readJSON("tables.json")
SUCCESS = 0
ERROR = -1

connection = None
cursor = None

# ===================== UTILITIES ===================== #

def executeQuery(query):
    try:
        cursor.execute(query)
        log.debug(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to execute query:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None
    return SUCCESS

# ===================== SELECT ===================== #

def location_exists(location_id):
    query = db.select("Location", where = f"location_id = '{location_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to determine existence of location with ID '{location_id}'")
        return False
    result = cursor.fetchall()
    return len(result) != 0

#check if person with the ID already exists
def person_exists(person_id):
    query = db.select("Person", where = f"person_id = '{person_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to determine existence of person with ID '{person_id}'")
        return False
    result = cursor.fetchall()
    return len(result) != 0

def code_exists(code, organization):
    query = db.select("Code", where = f"code = '{code}' and organization = '{organization}'")
    if executeQuery(query) is None:
        log.error(f"Failed to determine existence of '{organization}' code '{code}'")
        return False
    result = cursor.fetchall()
    return len(result) != 0

# ===================== INSERT ===================== #

def insert_person(person):
    if person["first_name"] == "NULL":
        person["first_name"] = "Anonymous"
    if person["last_name"] == "NULL":
        person["last_name"] = "Anonymous"

    query = db.insert(
        "Person",
        first_name = person["first_name"],
        last_name = person["last_name"],
        phone_number = person["phone_number"],
        age_range = person["age_range"],
        gender = person["gender"],
        ethnicity = person["ethnicity"]
    )

    if executeQuery(query) is None:
        return None

    person_id = cursor.lastrowid
    return person_id

# def insert_location(location):
#     query = db.insert(
#         "Location",
#         latitude = location["latitude"],
#         longitude = location["longitude"],
#         premises = location["premises"],
#         area = location["area"],
#         precinct = location["precinct"],
#         ward = location["ward"],
#         borough = location["borough"],
#         city = location["city"],
#         state = location["state"],
#         country = location["country"]
#     )

#     if executeQuery(query) is None:
#         return None

#     location_id = cursor.lastrowid
#     #return location_id

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

    if executeQuery(query) is None:
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

    if executeQuery(query) is None:
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

    if executeQuery(query) is None:
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

    if executeQuery(query) is None:
        return None

    search_id = cursor.lastrowid
    return search_id

def insert_code(code):
    #check if the code and Organization already exists
    code_value = code['code']
    organization = code['organization']

    query = db.select(
        "Code",
        f"code = '{code_value}' and organization = '{organization}'",
    )

    if executeQuery(query) is None:
        return None

    result = cursor.fetchall()
    if(len(result)):
        log.error(f"'{organization}' code '{code_value}' already exists")
        return None

    # add the code to the DB
    query = db.insert(
        "Code",
        code = code["code"],
        organization = code["organization"],
        category = code["category"],
        description = code["description"]
    )

    if executeQuery(query) is None:
        return None

    return SUCCESS

def insert_location(location):
    #check if the latitude and longitude already exists
    latitude = location["latitude"]
    longitude = location["longitude"]

    query = db.select(
        "Location",
        f"latitude = '{latitude}' and longitude = '{longitude}'"
    )

    if executeQuery(query) is None:
        return None

    result = cursor.fetchall()
    if(len(result)):
        log.error(f"Latitude: '{latitude}' with Longitude: '{longitude}' already exists")
        return None

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

    if executeQuery(query) is None:
        return None

    location_id = cursor.lastrowid
    return location_id

# ===================== CREATION ===================== #

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

# ===================== ADD ===================== #

def prompt_attributes(table, ignore = []):
    log.info(f"{table}:")
    record = {}
    for attribute in TABLES[table]:
        if attribute in ignore:
            continue
        value = input(f"{attribute}: ")
        if value == "":
            value = 'NULL'
        record[attribute] = value
    return record

def add_location_help_message():
    log.info(f"Please add a new location using '{INTERPRETER} {PROGRAM} add location'")

def add_person_help_message():
    log.info(f"Please add a new person using '{INTERPRETER} {PROGRAM} add person'")

def add_code_help_message():
    log.info(f"Please add a new code using '{INTERPRETER} {PROGRAM} add code'")

def add_incident():
    if no("Do you know the location ID for this incident?"):
        add_location_help_message()
        return None

    location_id = input("location_id: ")
    if not location_exists(location_id):
        log.error(f"Location with ID '{location_id}' not found!")
        add_location_help_message()
        return None

    incident = prompt_attributes('Incident', ignore = ['location_id', 'incident_id'])
    incident['location_id'] = location_id

    incident_id = insert_incident(incident)
    if incident_id is None:
        log.error("Failed to insert incident")
        return None

    return incident_id

def add_complaint():
    if no("Do you know the code and organization for this crime?"):
        add_code_help_message()
        return ERROR

    code = input("code: ")
    organization = input("organization: ")
    if not code_exists(code, organization):
        log.error(f"'{organization}' code '{code}' not found!")
        add_code_help_message()
        return ERROR

    incident_id = add_incident()
    if incident_id is None:
        return ERROR

    complaint = prompt_attributes('Complaint', ignore = ['complaint_id', 'incident_id', 'code', 'organization'])
    complaint['incident_id'] = incident_id
    complaint["code"] = code
    complaint["organization"] = organization

    complaint_id = insert_complaint(complaint)
    if complaint_id is None:
        log.error("Failed to insert complaint")
        return ERROR

    log.success(f"Added complaint '{complaint_id}' to database")
    return SUCCESS

def add_crime():
    if no("Do you know the ID of the victim?"):
        add_person_help_message()
        return ERROR

    victim_id = input("victim_id: ")
    if not person_exists(victim_id):
        log.error(f"Person with ID '{victim_id}' not found")
        add_person_help_message()
        return ERROR

    if no("Do you know the code and organization for this crime?"):
        add_code_help_message()
        return ERROR

    code = input("code: ")
    organization = input("organization: ")
    if not code_exists(code, organization):
        log.error(f"'{organization}' code '{code}' not found!")
        add_code_help_message()
        return ERROR

    incident_id = add_incident()
    if incident_id is None:
        return ERROR

    crime = prompt_attributes('Crime', ignore = ['crime_id', 'incident_id', 'victim_id', 'code', 'organization'])
    crime['victim_id'] = victim_id
    crime['code'] = code
    crime['organization'] = organization
    crime['incident_id'] = incident_id

    crime_id = insert_crime(crime)
    if crime_id is None:
        log.error("Failed to insert crime")
        return ERROR

    log.success(f"Added crime '{crime_id}' to database")
    return SUCCESS

def add_search():
    if no("Do you know the ID of the suspect?"):
        add_person_help_message()
        return ERROR

    suspect_id = input("suspect_id: ")
    if not person_exists(suspect_id):
        log.error(f"Person with ID '{suspect_id}' not found")
        add_person_help_message()
        return ERROR

    incident_id = add_incident()
    if incident_id is None:
        return ERROR

    search = prompt_attributes('Search', ignore = ['search_id', 'incident_id', 'suspect_id'])
    search['suspect_id'] = suspect_id
    search['incident_id'] = incident_id
    search_id = insert_search(search)

    if search_id is None:
        log.error("Failed to insert search")
        return ERROR

    log.success(f"Added search '{search_id}' to database")
    return SUCCESS

def add_location():
    location = prompt_attributes('Location', ignore = ['location_id'])

    location_id = insert_location(location)
    if location_id is None:
        log.error("Failed to insert location")
        return ERROR

    log.success(f"Added location with ID '{location_id}' (latitude: {location['latitude']}, longitude: {location['longitude']})")
    return SUCCESS

def add_code():
    code = prompt_attributes('Code')
    if code["code"] == "NULL" or code["organization"] == "NULL":
        log.error("code and organization cannot be NULL")
        return ERROR

    if insert_code(code) is None:
        log.error("Failed to insert code")
        return ERROR

    log.success(f"Added '{code['organization']}' code '{code['code']}'")
    return SUCCESS

def add_person():
    person = prompt_attributes('Person', ignore = ['person_id'])
    person_id = insert_person(person)

    if person_id is None:
        log.error(f"Failed to insert person")
        return ERROR

    log.success(f"Added person with ID '{person_id}' ({person['first_name']} {person['last_name']})")
    return SUCCESS

ADD_HELP = {
    "codes":     "Crime codes from a crime enforcement organization",
    "complaint": "Incidents reported to police",
    "crime":     "Crimes that have actually taken place",
    "search":    "Suspect who were detained and searched",
    "location":  "Location of a complaint, crime, or search",
    "person":    "Add a criminal or victim",
    "help":      "Show this message",
}

def help_add():
    log.info(f"{INTERPRETER} {PROGRAM} add code      : {ADD_HELP['codes']}")
    log.info(f"{INTERPRETER} {PROGRAM} add location  : {ADD_HELP['location']}")
    log.info(f"{INTERPRETER} {PROGRAM} add person    : {ADD_HELP['person']}")
    log.info(f"{INTERPRETER} {PROGRAM} add complaint : {ADD_HELP['complaint']}")
    log.info(f"{INTERPRETER} {PROGRAM} add crime     : {ADD_HELP['crime']}")
    log.info(f"{INTERPRETER} {PROGRAM} add search    : {ADD_HELP['search']}")
    log.info(f"{INTERPRETER} {PROGRAM} add help      : {ADD_HELP['help']}")

ADD_COMMANDS = {
    "code":      add_code,
    "location":  add_location,
    "person":    add_person,
    "complaint": add_complaint,
    "crime":     add_crime,
    "search":    add_search,
    "help":      help_add,
}

ADD_MIN_ARGC = 2
ADD_MAX_ARGC = 3

def add():
    if argc < ADD_MIN_ARGC or argc > ADD_MAX_ARGC:
        log.error(f"Incorrect number of arguments")
        help_add()
        return ERROR

    if argc == ADD_MIN_ARGC:
        command = "help"
    else:
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

if argc == MIN_ARGC:
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
