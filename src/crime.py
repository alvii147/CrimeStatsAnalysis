import log
import os
import transfer
import db
import utils

from sys import argv
from MySQLutils import connectDB, closeDB
from utils import yes, no, prompt_attribute, prompt_table, prompt_table_update, prompt_options

INTERPRETER = "python3"
PROGRAM = f"{INTERPRETER} {os.path.basename(argv[0])}"
SUCCESS = 0
ERROR = -1

connection = None
cursor = None

# ===================== UTILITIES ===================== #

def executeQuery(query):
    try:
        cursor.execute(query)
        #log.debug(f'Executing query "{consoleFriendly(query)}" ...')
    except Exception as e:
        log.error('Unable to execute query:')
        log.error(query)
        log.error('Exception:')
        log.error(e)
        return None
    return SUCCESS

# ===================== SELECT ===================== #

# --------------------- FIND --------------------- #

def find_complaint(complaint_id):
    query = db.select("Complaint", where = f"complaint_id = '{complaint_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to find complaint with ID '{complaint_id}'")
        return None
    return cursor.fetchall()

def find_crime(crime_id):
    query = db.select("Crime", where = f"crime_id = '{crime_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to find crime with ID '{crime_id}'")
        return None
    return cursor.fetchall()

def find_search(search_id):
    query = db.select("Search", where = f"search_id = '{search_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to find search with ID '{search_id}'")
        return None
    return cursor.fetchall()

def find_location(location_id):
    query = db.select("Location", where = f"location_id = '{location_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to find location with ID '{location_id}'")
        return None
    return cursor.fetchall()

def find_code(code, organization):
    query = db.select("Code", where = f"code = '{code}' and organization = '{organization}'")
    if executeQuery(query) is None:
        log.error(f"Failed to find '{organization}' code '{code}'")
        return None
    return cursor.fetchall()

def find_person(person_id):
    query = db.select("Person", where = f"person_id = '{person_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to find person with ID '{person_id}'")
        return None
    return cursor.fetchall()

def find_incident(incident_id):
    query = db.select("Incident", where = f"incident_id = '{incident_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to find incident with ID '{incident_id}'")
        return None
    return cursor.fetchall()

# --------------------- EXISTENCE --------------------- #

def location_exists(location_id):
    result = find_location(location_id)
    if result is None:
        return False
    return len(result) != 0

def person_exists(person_id):
    result = find_person(person_id)
    if result is None:
        return False
    return len(result) != 0

def code_exists(code, organization):
    result = find_code(code, organization)
    if result is None:
        return False
    return len(result) != 0

def incident_exists(incident_id):
    result = find_incident(incident_id)
    if result is None:
        return False
    return len(result) != 0

def crime_exists(crime_id):
    result = find_crime(crime_id)
    if result is None:
        return False
    return len(result) != 0

def search_exists(search_id):
    result = find_search(search_id)
    if result is None:
        return False
    return len(result) != 0

def complaint_exists(complaint_id):
    result = find_complaint(complaint_id)
    if result is None:
        return False
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

    query = db.select("Code", f"code = '{code_value}' and organization = '{organization}'",)
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

def create(args):
    queries = utils.loadQueries("SQL/create.sql")
    utils.runQueries(queries)

    queries = utils.loadQueries("SQL/keys.sql")
    utils.runQueries(queries)

    queries = utils.loadQueries("SQL/views.sql")
    utils.runQueries(queries)

def load(args):
    n = 1000
    if len(args) > 0:
        try:
            n = int(args[0])
        except:
            log.error('\'num_of_entries must be an integer\'')

    log.info(f'Loading {n} entries from each csv')
    queries = utils.loadQueries("SQL/create_temp.sql")
    utils.runQueries(queries)

    queries = utils.loadQueries("SQL/load.sql")
    queries = [db.loadReplaceIgnoreLines(query, n) for query in queries]
    utils.runQueries(queries)

    transfer.transfer_all()

    queries = utils.loadQueries("SQL/drop.sql")
    utils.runQueries(queries)

def clean(args):
    queries = utils.loadQueries("SQL/clean.sql")
    utils.runQueries(queries)

def clear(args):
    queries = utils.loadQueries("SQL/clear.sql")
    utils.runQueries(queries)

# ===================== ADD ===================== #

def add_location_help_message():
    log.info(f"Please add a new location using '{PROGRAM} add location'")

def add_person_help_message():
    log.info(f"Please add a new person using '{PROGRAM} add person'")

def add_code_help_message():
    log.info(f"Please add a new code using '{PROGRAM} add code'")

def add_incident():
    if no("Do you know the location ID for this incident?"):
        add_location_help_message()
        return None

    location_id = prompt_attribute("Incident", "location_id", db.TABLES)
    if not location_exists(location_id):
        log.error(f"Location with ID '{location_id}' not found!")
        add_location_help_message()
        return None

    incident = prompt_table('Incident', db.TABLES, ignore = ['location_id', 'incident_id'])
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

    code = prompt_attribute("Complaint", "code", db.TABLES)
    organization = prompt_attribute("Complaint", "organization", db.TABLES)
    if not code_exists(code, organization):
        log.error(f"'{organization}' code '{code}' not found!")
        add_code_help_message()
        return ERROR

    incident_id = add_incident()
    if incident_id is None:
        return ERROR

    complaint = prompt_table('Complaint', db.TABLES, ignore = ['complaint_id', 'incident_id', 'code', 'organization'])
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

    victim_id = prompt_attribute("Crime", "victim_id", db.TABLES)
    if not person_exists(victim_id):
        log.error(f"Person with ID '{victim_id}' not found")
        add_person_help_message()
        return ERROR

    if no("Do you know the code and organization for this crime?"):
        add_code_help_message()
        return ERROR

    code = prompt_attribute("Crime", "code", db.TABLES)
    organization = prompt_attribute("Crime", "organization", db.TABLES)
    if not code_exists(code, organization):
        log.error(f"'{organization}' code '{code}' not found!")
        add_code_help_message()
        return ERROR

    incident_id = add_incident()
    if incident_id is None:
        return ERROR

    crime = prompt_table('Crime', db.TABLES, ignore = ['crime_id', 'incident_id', 'victim_id', 'code', 'organization'])
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

    suspect_id = prompt_attribute("Search", "suspect_id", db.TABLES)
    if not person_exists(suspect_id):
        log.error(f"Person with ID '{suspect_id}' not found")
        add_person_help_message()
        return ERROR

    incident_id = add_incident()
    if incident_id is None:
        return ERROR

    search = prompt_table('Search', db.TABLES, ignore = ['search_id', 'incident_id', 'suspect_id'])
    search['suspect_id'] = suspect_id
    search['incident_id'] = incident_id
    search_id = insert_search(search)

    if search_id is None:
        log.error("Failed to insert search")
        return ERROR

    log.success(f"Added search '{search_id}' to database")
    return SUCCESS

def add_location():
    location = prompt_table('Location', db.TABLES, ignore = ['location_id'])

    location_id = insert_location(location)
    if location_id is None:
        log.error("Failed to insert location")
        return ERROR

    log.success(f"Added location with ID '{location_id}' (latitude: {location['latitude']}, longitude: {location['longitude']})")
    return SUCCESS

def add_code():
    code = prompt_table('Code', db.TABLES)
    if code["code"] == "NULL" or code["organization"] == "NULL":
        log.error("code and organization cannot be NULL")
        return ERROR

    if insert_code(code) is None:
        log.error("Failed to insert code")
        return ERROR

    log.success(f"Added '{code['organization']}' code '{code['code']}'")
    return SUCCESS

def add_person():
    person = prompt_table('Person', db.TABLES, ignore = ['person_id'])
    person_id = insert_person(person)

    if person_id is None:
        log.error(f"Failed to insert person")
        return ERROR

    log.success(f"Added person with ID '{person_id}' ({person['first_name']} {person['last_name']})")
    return SUCCESS

ADD_HELP = {
    "code":      "Add a crime code from a crime enforcement organization",
    "complaint": "Add a complaint that was made to the police",
    "crime":     "Add a crimes that has taken place",
    "search":    "Add a suspect search record",
    "location":  "Add a location of a complaint, crime, or search",
    "person":    "Add a suspect or victim",
    "help":      "Show this message",
}

def help_add():
    log.info(f"{PROGRAM} add code      : {ADD_HELP['code']}")
    log.info(f"{PROGRAM} add location  : {ADD_HELP['location']}")
    log.info(f"{PROGRAM} add person    : {ADD_HELP['person']}")
    log.info(f"{PROGRAM} add complaint : {ADD_HELP['complaint']}")
    log.info(f"{PROGRAM} add crime     : {ADD_HELP['crime']}")
    log.info(f"{PROGRAM} add search    : {ADD_HELP['search']}")
    log.info(f"{PROGRAM} add help      : {ADD_HELP['help']}")

def usage_add():
    log.info(f"{PROGRAM} add <command>")
    log.info(f"Try '{PROGRAM} add help'")

ADD_COMMANDS = {
    "code":      add_code,
    "location":  add_location,
    "person":    add_person,
    "complaint": add_complaint,
    "crime":     add_crime,
    "search":    add_search,
    "help":      help_add,
}

ADD_MIN_ARGC = 0
ADD_MAX_ARGC = 1

def add(args):
    argc = len(args)
    if argc < ADD_MIN_ARGC or argc > ADD_MAX_ARGC:
        log.error("Incorrect number of arguments")
        usage_add()
        return ERROR

    command = "help"   # default

    if argc == 1:
        command = args[0]

    if command not in ADD_COMMANDS:
        log.error(f"Unknown command '{command}'")
        usage_add()
        return ERROR

    return ADD_COMMANDS[command]()

# ===================== DELETE ===================== #

def usage_delete():
    log.info(f"{PROGRAM} delete <command> [arguments]")
    log.info(f"Try '{PROGRAM} delete help'")

def delete_code(args):
    if len(args) != 2:
        log.error("Incorrect number of arguments")
        usage_delete()
        return ERROR
    code = args[0]
    organization = args[1]

    if not code_exists(code, organization):
        log.error(f"No such '{organization}' code '{code}'")
        return ERROR

    query = db.select("Complaint", where = f"code = '{code}' and organization = '{organization}'")
    if executeQuery(query) is None:
        log.error(f"Failed to query for complaints with '{organization}' code '{code}'")
        return ERROR
    complaints = cursor.fetchall()
    if len(complaints) != 0:
        log.error(f"{len(complaints)} complaints use this code")
        log.info(f"Delete these complaints before attempting to delete '{organization}' code '{code}'")
        return ERROR

    query = db.select("Crime", where = f"code = '{code}' and organization = '{organization}'")
    if executeQuery(query) is None:
        log.error(f"Failed to query for crimes with '{organization}' code '{code}'")
        return ERROR
    crimes = cursor.fetchall()
    if len(crimes) != 0:
        log.error(f"{len(crimes)} crimes use this code")
        log.info(f"Delete these crimes before attempting to delete '{organization}' code '{code}'")
        return ERROR

    query = db.delete("Code", where = f"code = '{code}' and organization = '{organization}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete '{organization}' code '{code}'")
        return ERROR

    log.success(f"Deleted '{organization}' code '{code}'")
    return SUCCESS

def delete_location(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_delete()
        return ERROR
    location_id = args[0]

    if not location_exists(location_id):
        log.error(f"No such location with ID '{location_id}'")
        return ERROR

    query = db.select("Incident", where = f"location_id = '{location_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to query for incidents at location '{location_id}'")
        return ERROR
    incidents = cursor.fetchall()

    if len(incidents) != 0:
        log.error(f"{len(incidents)} incidents refer to this location")
        log.info(f"Delete these incidents before attempting to delete location '{location_id}'")
        return ERROR

    query = db.delete("Location", where = f"location_id = '{location_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete location '{location_id}'")
        return ERROR

    log.success(f"Deleted location '{location_id}'")
    return SUCCESS

def delete_person(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_delete()
        return ERROR
    person_id = args[0]

    if not person_exists(person_id):
        log.error(f"No such person with ID '{person_id}'")
        return ERROR

    query = db.select("Crime", where = f"victim_id = '{person_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to query for crimes where person '{person_id}' was a victim")
        return ERROR
    crimes = cursor.fetchall()
    if len(crimes) != 0:
        log.error(f"{len(crimes)} crimes refer to this person")
        log.info(f"Delete these crimes before attempting to delete person '{person_id}'")
        return ERROR

    query = db.select("Search", where = f"suspect_id = '{person_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to query for searches where person '{person_id}' was a suspect")
        return ERROR
    searches = cursor.fetchall()
    if len(searches) != 0:
        log.error(f"{len(searches)} searches refer to this person")
        log.info(f"Delete these searches before attempting to delete person '{person_id}'")
        return ERROR

    query = db.delete("Person", where = f"person_id = '{person_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete person '{person_id}'")
        return ERROR

    log.success(f"Deleted person '{person_id}'")
    return SUCCESS

def delete_complaint(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_delete()
        return ERROR
    complaint_id = args[0]

    complaint = find_complaint(complaint_id)
    if complaint is None:
        return ERROR

    if len(complaint) == 0:
        log.error(f"No such complaint with ID '{complaint_id}'")
        return ERROR

    incident_id = complaint[0][1]
    incident = find_incident(incident_id)
    if incident is None:
        return ERROR

    if len(incident) == 0:
        log.error(f"No such incident with ID '{incident_id}' corresponding to complaint '{complaint_id}'")
        return ERROR

    query = db.delete("Complaint", where = f"complaint = '{complaint}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete complaint with ID '{complaint_id}'")
        return ERROR

    query = db.delete("Incident", where = f"incident_id = '{incident_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete incident with ID '{incident_id}'")
        return ERROR

    log.success(f"Deleted complaint '{complaint_id}'")
    return SUCCESS

def delete_crime(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_delete()
        return ERROR
    crime_id = args[0]

    crime = find_crime(crime_id)
    if crime is None:
        return ERROR

    if len(crime) == 0:
        log.error(f"No such crime with ID '{crime_id}'")
        return ERROR

    incident_id = crime[0][1]
    incident = find_incident(incident_id)
    if incident is None:
        return ERROR

    if len(incident) == 0:
        log.error(f"No such incident with ID '{incident_id}' corresponding to crime '{crime_id}'")
        return ERROR

    query = db.delete("Crime", where = f"crime_id = '{crime_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete crime with ID '{crime_id}'")
        return ERROR

    query = db.delete("Incident", where = f"incident_id = '{incident_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete incident with ID '{incident_id}'")
        return ERROR

    log.success(f"Deleted crime '{crime_id}'")
    return SUCCESS

def delete_search(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_delete()
        return ERROR
    search_id = args[0]

    search = find_search(search_id)
    if search is None:
        return ERROR

    if len(search) == 0:
        log.error(f"No such search with ID '{search_id}'")
        return ERROR

    incident_id = search[0][1]
    incident = find_incident(incident_id)
    if incident is None:
        return ERROR

    if len(incident) == 0:
        log.error(f"No such incident with ID '{search_id}' corresponding to search '{search_id}'")
        return ERROR

    query = db.delete("Search", where = f"search_id = '{search_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete search with ID '{search_id}'")
        return ERROR

    query = db.delete("Incident", where = f"incident_id = '{incident_id}'")
    if executeQuery(query) is None:
        log.error(f"Failed to delete incident with ID '{incident_id}'")
        return ERROR

    log.success(f"Deleted search '{search_id}'")
    return SUCCESS

DELETE_HELP = {
    "code":      "Delete a code from a crime enforcement organization",
    "complaint": "Delete a police complaint record",
    "crime":     "Delete a crime record",
    "search":    "Delete a suspect search record",
    "location":  "Delete a location",
    "person":    "Delete a person",
    "help":      "Show this message",
}

def help_delete(args):
    log.info(f"{PROGRAM} delete code      <code> <organization> : {DELETE_HELP['code']}")
    log.info(f"{PROGRAM} delete location  <location_id>         : {DELETE_HELP['location']}")
    log.info(f"{PROGRAM} delete person    <person_id>           : {DELETE_HELP['person']}")
    log.info(f"{PROGRAM} delete complaint <complaint_id>        : {DELETE_HELP['complaint']}")
    log.info(f"{PROGRAM} delete crime     <crime_id>            : {DELETE_HELP['crime']}")
    log.info(f"{PROGRAM} delete search    <search_id>           : {DELETE_HELP['search']}")
    log.info(f"{PROGRAM} delete help                            : {DELETE_HELP['help']}")

DELETE_COMMANDS = {
    "code":      delete_code,
    "location":  delete_location,
    "person":    delete_person,
    "complaint": delete_complaint,
    "crime":     delete_crime,
    "search":    delete_search,
    "help":      help_delete,
}

DELETE_MIN_ARGC = 0
DELETE_MAX_ARGC = 3

def delete(args):
    argc = len(args)
    if argc < DELETE_MIN_ARGC or argc > DELETE_MAX_ARGC:
        log.error("Incorrect number of arguments")
        usage_delete()
        return ERROR

    # default
    command = "help"
    if argc > 0:
        command = args[0]
    args = args[1:]

    if command not in DELETE_COMMANDS:
        log.error(f"Unknown command '{command}'")
        usage_delete()
        return ERROR

    return DELETE_COMMANDS[command](args)

# ===================== UPDATE ===================== #

def usage_update():
    log.info(f"{PROGRAM} update <command> [arguments]")
    log.info(f"Try '{PROGRAM} update help'")

def update_code(args):
    if len(args) != 2:
        log.error("Incorrect number of arguments")
        usage_update()
        return ERROR
    code = args[0]
    organization = args[1]

    if not code_exists(code, organization):
        log.error(f"No such '{organization}' code '{code}'")
        return ERROR

    updates = prompt_table_update("Code", db.TABLES, ignore = ["code", "organization"])

    if len(updates) != 0:
        query = db.update("Code", where = f"code = '{code}' and organization = '{organization}'", **updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update '{organization}' code '{code}'")
            return ERROR
        log.success(f"Updated '{organization}' code '{code}'")

    return SUCCESS

def update_location(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_update()
        return ERROR
    location_id = args[0]

    if not location_exists(location_id):
        log.error(f"No such location with ID '{location_id}'")
        return ERROR

    updates = prompt_table_update("Location", db.TABLES, ignore = ["location_id"])

    if len(updates) != 0:
        query = db.update("Location", where = f"location_id = '{location_id}'", **updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update location '{location_id}'")
            return ERROR
        log.success(f"Updated location '{location_id}'")

    return SUCCESS

def update_person(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_update()
        return ERROR
    person_id = args[0]

    if not person_exists(person_id):
        log.error(f"No such person with ID '{person_id}'")
        return ERROR

    updates = prompt_table_update("Person", db.TABLES, ignore = ["person_id"])

    if len(updates) != 0:
        query = db.update("Person", where = f"person_id = '{person_id}'", **updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update person '{person_id}'")
            return ERROR
        log.success(f"Updated person '{person_id}'")

    return SUCCESS

def update_complaint(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_update()
        return ERROR
    complaint_id = args[0]

    complaint = find_complaint(complaint_id)
    if complaint is None:
        return ERROR

    if len(complaint) == 0:
        log.error(f"No such complaint with ID '{complaint_id}'")
        return ERROR

    incident_id = complaint[0][1]
    incident = find_incident(incident_id)
    if incident is None:
        return ERROR

    if len(incident) == 0:
        log.error(f"No such incident with ID '{incident_id}' corresponding to complaint '{complaint_id}'")
        return ERROR

    incident_updates = prompt_table_update("Incident", db.TABLES, ignore = ["incident_id"])
    complaint_updates = prompt_table_update("Complaint", db.TABLES, ignore = ["incident_id", "complaint_id"])

    # check if the updates break any foreign keys
    if "location_id" in incident_updates:
        location_id = incident_updates["location_id"]
        if not location_exists(location_id):
            log.error(f"No such location with ID '{location_id}'")
            return ERROR

    if "code" in complaint_updates or "organization" in complaint_updates:
        code = complaint_updates["code"]
        organization = complaint_updates["organization"]
        if not code_exists(code, organization):
            log.error(f"No such '{organization}' code '{code}'")
            return ERROR

    # apply updates if there are any
    if len(incident_updates) != 0:
        query = db.update("Incident", where = f"incident_id = '{incident_id}'", **incident_updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update incident '{incident_id}'")
            return ERROR
        log.success(f"Updated incident '{incident_id}'")

    if len(complaint_updates) != 0:
        query = db.update("Complaint", where = f"complaint_id = '{complaint_id}'", **complaint_updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update complaint '{complaint_id}'")
            return ERROR
        log.success(f"Updated complaint '{complaint_id}'")

    return SUCCESS

def update_crime(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_update()
        return ERROR
    crime_id = args[0]

    crime = find_crime(crime_id)
    if crime is None:
        return ERROR

    if len(crime) == 0:
        log.error(f"No such crime with ID '{crime_id}'")
        return ERROR

    incident_id = crime[0][1]
    incident = find_incident(incident_id)
    if incident is None:
        return ERROR

    if len(incident) == 0:
        log.error(f"No such incident with ID '{incident_id}' corresponding to crime '{crime_id}'")
        return ERROR

    incident_updates = prompt_table_update("Incident", db.TABLES, ignore = ["incident_id"])
    crime_updates = prompt_table_update("Crime", db.TABLES, ignore = ["incident_id", "crime_id"])

    # check if the updates break any foreign keys
    if "location_id" in incident_updates:
        location_id = incident_updates["location_id"]
        if not location_exists(location_id):
            log.error(f"No such location with ID '{location_id}'")
            return ERROR

    if "code" in crime_updates or "organization" in crime_updates:
        code = crime_updates["code"]
        organization = crime_updates["organization"]
        if not code_exists(code, organization):
            log.error(f"No such '{organization}' code '{code}'")
            return ERROR

    if "victim_id" in crime_updates:
        victim_id = crime_updates["victim_id"]
        if not person_exists(victim_id):
            log.error(f"No such victim with ID '{victim_id}'")
            return ERROR

    # apply updates if there are any
    if len(incident_updates) != 0:
        query = db.update("Incident", where = f"incident_id = '{incident_id}'", **incident_updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update incident '{incident_id}'")
            return ERROR
        log.success(f"Updated incident '{incident_id}'")

    if len(crime_updates) != 0:
        query = db.update("Complaint", where = f"crime_id = '{crime_id}'", **crime_updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update complaint '{crime_id}'")
            return ERROR
        log.success(f"Updated crime '{crime_id}'")

    return SUCCESS

def update_search(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_update()
        return ERROR
    search_id = args[0]

    search = find_search(search_id)
    if search is None:
        return ERROR

    if len(search) == 0:
        log.error(f"No such search with ID '{search_id}'")
        return ERROR

    incident_id = search[0][1]
    incident = find_incident(incident_id)
    if incident is None:
        return ERROR

    if len(incident) == 0:
        log.error(f"No such incident with ID '{search_id}' corresponding to search '{search_id}'")
        return ERROR

    incident_updates = prompt_table_update("Incident", db.TABLES, ignore = ["incident_id"])
    search_updates = prompt_table_update("Search", db.TABLES, ignore = ["search_id", "incident_id"])

    # check if the updates break any foreign keys
    if "location_id" in incident_updates:
        location_id = incident_updates["location_id"]
        if not location_exists(location_id):
            log.error(f"No such location with ID '{location_id}'")
            return ERROR

    if "suspect_id" in search_updates:
        suspect_id = search_updates["suspect_id"]
        if not person_exists(suspect_id):
            log.error(f"No such suspect with ID '{suspect_id}'")
            return ERROR

    # apply updates if there are any
    if len(incident_updates) != 0:
        query = db.update("Incident", where = f"incident_id = '{incident_id}'", **incident_updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update incident '{incident_id}'")
            return ERROR
        log.success(f"Updated incident '{incident_id}'")

    if len(search_updates) != 0:
        query = db.update("Search", where = f"search_id = '{search_id}'", **search_updates)
        if executeQuery(query) is None:
            log.error(f"Failed to update search '{search_id}'")
            return ERROR
        log.success(f"Updated search '{search_id}'")

    return SUCCESS

UPDATE_HELP = {
    "code":      "Update information about a crime code",
    "complaint": "Update details of a police complaint",
    "crime":     "Update details of a crime record",
    "search":    "Update details of a suspect search",
    "location":  "Update location details",
    "person":    "Update information about a person",
    "help":      "Show this message",
}

def help_update(args):
    log.info(f"{PROGRAM} update code      <code> <organization> : {UPDATE_HELP['code']}")
    log.info(f"{PROGRAM} update location  <location_id>         : {UPDATE_HELP['location']}")
    log.info(f"{PROGRAM} update person    <person_id>           : {UPDATE_HELP['person']}")
    log.info(f"{PROGRAM} update complaint <complaint_id>        : {UPDATE_HELP['complaint']}")
    log.info(f"{PROGRAM} update crime     <crime_id>            : {UPDATE_HELP['crime']}")
    log.info(f"{PROGRAM} update search    <search_id>           : {UPDATE_HELP['search']}")
    log.info(f"{PROGRAM} update help                            : {UPDATE_HELP['help']}")

UPDATE_COMMANDS = {
    "code":      update_code,
    "location":  update_location,
    "person":    update_person,
    "complaint": update_complaint,
    "crime":     update_crime,
    "search":    update_search,
    "help":      help_update,
}

UPDATE_MIN_ARGC = 0
UPDATE_MAX_ARGC = 3

def update(args):
    argc = len(args)
    if argc < UPDATE_MIN_ARGC or argc > UPDATE_MAX_ARGC:
        log.error("Incorrect number of arguments")
        usage_update()
        return ERROR

    # default
    command = "help"
    if argc > 0:
        command = args[0]
    args = args[1:]

    if command not in UPDATE_COMMANDS:
        log.error(f"Unknown command '{command}'")
        usage_update()
        return ERROR

    return UPDATE_COMMANDS[command](args)

# ================== BACKGROUND ================== #

def background_id():
    person_id = input('Enter ID: ')
    try:
        person_id = int(person_id)
    except ValueError:
        log.error('Please enter numeric value for ID')
        return ERROR

    person_attributes = list(db.TABLES['Person'].keys())
    query = db.select(
        'Person',
        where=f'person_id = {person_id}',
        attributes=person_attributes,
    )

    return query

def background_name():
    first_name = input('First Name: ')
    last_name = input('Last Name: ')
    empty_first_name = len(first_name.strip()) > 0
    empty_last_name = len(last_name.strip()) > 0

    where = ''
    if empty_first_name:
        where += f'first_name LIKE \'%{first_name}%\''

    if empty_last_name:
        if empty_first_name:
            where += ' AND '

        where += f'last_name LIKE \'%{last_name}%\''

    person_attributes = list(db.TABLES['Person'].keys())
    query = db.select(
        'Person',
        where=where,
        attributes=person_attributes,
    )

    return query

def background_get_search_method():
    message = 'Search for person by:'
    options = [
        'ID',
        'First & Last Names',
    ]

    try:
        selection_idx = prompt_options(options, message=message)
    except:
        log.error('Invalid selection')
        return ERROR

    if selection_idx == 0:
        return 'id'
    elif selection_idx == 1:
        return 'name'

    return ERROR

BACKGROUND_HELP = {
    "id":       "Run background check based on person ID",
    "name":     "Run background check based on first and last names",
}

def help_background():
    log.info(f"{PROGRAM} background id   : {BACKGROUND_HELP['id']}")
    log.info(f"{PROGRAM} background name : {BACKGROUND_HELP['name']}")

def usage_background():
    log.info(f"{PROGRAM} background <command> [arguments]")
    log.info(f"Try '{PROGRAM} background help'")

BACKGROUND_COMMANDS = {
    "id":   background_id,
    "name": background_name,
    "help": help_background,
}

BACKGROUND_MIN_ARGC = 0
BACKGROUND_MAX_ARGC = 1

def background(args):
    argc = len(args)
    if argc < BACKGROUND_MIN_ARGC or argc > BACKGROUND_MAX_ARGC:
        log.error("Incorrect number of arguments")
        usage_background()
        return ERROR

    if argc == 1:
        command = args[0]
        if command not in BACKGROUND_COMMANDS:
            log.error(f"Unknown command '{command}'")
            usage_background()
            return ERROR
    else:
        command = background_get_search_method()
        if isinstance(command, int) and command == ERROR:
            return ERROR

    if command == "help":
        return BACKGROUND_COMMANDS["help"]()

    query = BACKGROUND_COMMANDS[command]()
    if isinstance(query, int) and query == ERROR:
        return ERROR

    executeQuery(query)
    output = cursor.fetchall()

    log.info(f'Search returned {len(output)} results')

    if len(output) < 1:
        return ERROR

    options = [' '.join([o[1].strip(), o[2].strip()]) for o in output]
    message = 'Select person to run a background check on'

    try:
        selection_idx = prompt_options(options, message=message)
    except:
        log.error('Invalid selection')
        return ERROR

    if selection_idx == len(options):
        return ERROR

    person = output[selection_idx]
    person_attributes = list(db.TABLES['Person'].keys())
    person_id = person[person_attributes.index('person_id')]
    person_first_name = person[person_attributes.index('first_name')]
    person_last_name = person[person_attributes.index('last_name')]
    person_name = ' '.join([person_first_name.strip(), person_last_name.strip()])

    crime_view_attributes = list(db.TABLES['CrimeView'].keys())
    query = db.select(
        'CrimeView',
        where=f'victim_id = {person_id}',
        attributes=crime_view_attributes,
    )
    executeQuery(query)
    person_crimes = cursor.fetchall()

    search_view_attributes = list(db.TABLES['SearchView'].keys())
    query = db.select(
        'SearchView',
        where=f'suspect_id = {person_id}',
        attributes=search_view_attributes,
    )
    executeQuery(query)
    person_searches = cursor.fetchall()

    print('')
    log.info('---------------------------------------------------------')
    log.info(f'Person information for {person_name}:')
    log.info('---------------------------------------------------------')
    for i, val in enumerate(person):
        log.info(person_attributes[i] + ': ' + str(val))
    log.info('---------------------------------------------------------')

    print('')
    log.info('---------------------------------------------------------')
    log.info(f'{person_name} was a victim of the following crimes:')
    log.info('---------------------------------------------------------')
    for row in person_crimes:
        for i, val in enumerate(row):
            log.info(crime_view_attributes[i] + ': ' + str(val))
        log.info('---------------------------------------------------------')

    if len(person_crimes) < 1:
        log.info('No crime records found')

    print('')
    log.info('---------------------------------------------------------')
    log.info(f'{person_name} was searched as a suspect of the following crimes:')
    log.info('---------------------------------------------------------')
    for i, row in enumerate(person_searches):
        for i, val in enumerate(row):
            log.info(search_view_attributes[i] + ': ' + str(val))
        log.info('---------------------------------------------------------')

    if len(person_searches) < 1:
        log.info('No stop & search records found')

    return SUCCESS

# ================== SHOW ================== #

def print_table(records):
    paddings = [0] * len(records[0])
    for r in range(len(records)):
        for c in range(len(records[r])):
            value = records[r][c]
            if value != None:
                paddings[c] = max(paddings[c], len(str(value)))

    for r in range(len(records)):
        if r == 0:
            print("\n|", end="")
            for c in range(len(records[r])):
                print(" %s |" % ("-" * paddings[c]), end = "")
            print("")

        print("|", end = "")
        for c in range(len(records[r])):
            value = records[r][c]
            if value is None:
                value = "NULL"
            print(" %-*s |" % (paddings[c], str(value)), end = "")

        if r == 0 or r == len(records) - 1:
            print("\n|", end="")
            for c in range(len(records[r])):
                print(" %s |" % ("-" * paddings[c]), end = "")

        print("")

def show_code(args):
    organization = None
    code = None

    if yes("Do you know the crime code?"):
        code = prompt_attribute("Code", "code", db.TABLES)
    if yes("Do you know the name of the crime enforcement organization?"):
        organization = prompt_attribute("Code", "organization", db.TABLES)

    if code == None and organization == None:
        query = "SELECT * from Code;"
    elif code == None and organization != None:
        query = db.select("Code", f"organization = '{organization}'")
    elif code != None and organization == None:
        query = db.select("Code", f"code = '{code}'")
    else:
        query = db.select("Code", f"code = '{code}' and organization = '{organization}'")

    if executeQuery(query) is None:
        log.error(f"Failed to query for codes")
        return ERROR

    results = cursor.fetchall()
    if len(results) == 0:
        log.info("No codes found")
        return SUCCESS

    headers =  [('Code','Organization','Category','Description')]
    print_table(headers + results)

    return SUCCESS

def show_person(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_show()
        return ERROR
    person_id = args[0]

    query = db.select("Person", f"person_id = {person_id}")
    if executeQuery(query) is None:
        log.error(f"Failed to query for Person")
        return ERROR

    results = cursor.fetchall()
    header = [('Person ID', 'First Name', 'Last Name', 'Age', 'Gender', 'Ethnicity', 'Primary Phone Number')]
    print_table(header + results)

    return SUCCESS

def show_location(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_show()
        return ERROR
    location_id = args[0]

    query = db.select("Location", f"location_id = {location_id}")
    if executeQuery(query) is None:
        log.error(f"Failed to query for Location")
        return ERROR

    results = cursor.fetchall()
    header = [('Location ID','Latitude', 'Longitude', 'Premises', 'Area', 'Precinct', 'Ward', 'Borough', 'City', 'State', 'Country')]
    print_table(header + results)

    return SUCCESS

def show_complaint(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_show()
        return ERROR
    complaint_id = args[0]

    query = db.select("Complaint", f"complaint_id = {complaint_id}")
    if executeQuery(query) is None:
        log.error(f"Failed to query for complaint")
        return ERROR

    results = cursor.fetchall()
    header = [('Complaint ID', 'Incident ID', 'Code', 'Organization', 'Reported Date', 'Description')]
    print_table(header + results)

    return SUCCESS

def show_crime(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_show()
        return ERROR
    crime_id = args[0]

    query = db.select("Crime", f"crime_id = {crime_id}")
    if executeQuery(query) is None:
        log.error(f"Failed to query for crime")
        return ERROR

    results = cursor.fetchall()
    header = [('Crime ID', 'Incident ID', 'Code', 'Organization', 'VictimID', 'Weapon', 'Domestic', 'Description')]
    print_table(header + results)

    return SUCCESS

def show_search(args):
    if len(args) != 1:
        log.error("Incorrect number of arguments")
        usage_show()
        return ERROR
    search_id = args[0]

    query = db.select("Search", f"search_id = {search_id}")
    if executeQuery(query) is None:
        log.error(f"Failed to query for Search")
        return ERROR

    results = cursor.fetchall()
    header = [('Search ID', 'Incident ID', 'Suspect ID', 'Legislation', 'Object', 'Outcome', 'Object_caused_outcome', 'Clothing_removal')]
    print_table(header + results)

    return SUCCESS

SHOW_HELP = {
    "code":      "Show information about an organization's crime code",
    "person":    "Show information about a person",
    "location":  "Show information about a location",
    "complaint": "Show information about a complaint",
    "search":    "Show information about a search",
    "crime":     "Show information about a crime",
    "help":      "Show this message",
}

def help_show(args):
    log.info(f"{PROGRAM} show code                     : {SHOW_HELP['code']}")
    log.info(f"{PROGRAM} show person    <person_id>    : {SHOW_HELP['person']}")
    log.info(f"{PROGRAM} show location  <location_id>  : {SHOW_HELP['location']}")
    log.info(f"{PROGRAM} show complaint <complaint_id> : {SHOW_HELP['complaint']}")
    log.info(f"{PROGRAM} show search    <search_id>    : {SHOW_HELP['search']}")
    log.info(f"{PROGRAM} show crime     <crime_id>     : {SHOW_HELP['crime']}")
    log.info(f"{PROGRAM} show help                     : {SHOW_HELP['help']}")

def usage_show():
    log.info(f"{PROGRAM} show <command> [arguments]")
    log.info(f"Try '{PROGRAM} show help'")

SHOW_COMMANDS = {
    "code":      show_code,
    "help":      help_show,
    "person":    show_person,
    "location":  show_location,
    "crime":     show_crime,
    "complaint": show_complaint,
    "search":    show_search
}

SHOW_MIN_ARGC = 0
SHOW_MAX_ARGC = 2

def show(args):
    argc = len(args)
    if argc < SHOW_MIN_ARGC or argc > SHOW_MAX_ARGC:
        log.error("Incorrect number of arguments")
        usage_show()
        return ERROR

    # default
    command = "help"
    if argc > 0:
        command = args[0]
    args = args[1:]

    if command not in SHOW_COMMANDS:
        log.error(f"Unknown command '{command}'")
        usage_show()
        return ERROR

    return SHOW_COMMANDS[command](args)

# ================== FILTER ================== #

def prompt_filters_location():
    clauses = []

    if yes("Do have a country you want to filter by? "):
        country = prompt_attribute("Location", "country", db.TABLES)
        if country != "NULL":
            clauses.append(f"country = '{country}'")

    if yes("Do have a city you want to filter by? "):
        city = prompt_attribute("Location", "city", db.TABLES)
        if city != "NULL":
            clauses.append(f"city = '{city}'")

    if yes("Do have a state you want to filter by? "):
        state = prompt_attribute("Location", "state", db.TABLES)
        if state != "NULL":
            clauses.append(f"state = '{state}'")

    if yes("Do have a borough you want to filter by? "):
        borough = prompt_attribute("Location", "borough", db.TABLES)
        if borough != "NULL":
            clauses.append(f"borough = '{borough}'")

    if len(clauses) == 0:
        return None

    return " and ".join(clauses)

def prompt_filters_code():
    clauses = []

    if yes("Do you know the crime code?"):
        code = prompt_attribute("Code", "code", db.TABLES)
        if code != "NULL":
            clauses.append(f"code = '{code}'")

    if yes("Do you know the name of the crime enforcement organization?"):
        organization = prompt_attribute("Code", "organization", db.TABLES)
        if organization != "NULL":
            clauses.append(f"organization = '{organization}'")

    if len(clauses) == 0:
        return None

    return " and ".join(clauses)

def prompt_filters_date():
    clauses = []

    userChoice = 0
    log.info("[1] Filter by exact date")
    log.info("[2] Filter by date range")
    while userChoice != "1" and userChoice != "2":
        userChoice = input("Enter selection: ")

    if userChoice == "1":
        occurrence_date = prompt_attribute("Incident", "occurrence_date", db.TABLES)
        clauses.append(f"occurrence_date = '{occurrence_date}'")
    elif userChoice == "2":
        if yes("Do have a max date you want to filter by? "):
            occurrence_date = prompt_attribute("Incident", "occurrence_date", db.TABLES)
            if occurrence_date != "NULL":
                clauses.append(f"occurrence_date < '{occurrence_date}'")

        if yes("Do have a min date you want to filter by? "):
            occurrence_date = prompt_attribute("Incident", "occurrence_date", db.TABLES)
            if occurrence_date != "NULL":
                clauses.append(f"occurrence_date > '{occurrence_date}'")
    else:
        return None

    if len(clauses) == 0:
        return None

    return " and ".join(clauses)

def prompt_filters(location = True, code = True, date = True):
    clauses = []

    if location:
        if yes("Do you want to filter by location? "):
            location = prompt_filters_location()
            if location is not None:
                clauses.append(location)

    if code:
        if yes("Do you want to filter by code? "):
            code = prompt_filters_code()
            if code is not None:
                clauses.append(code)

    if date:
        if yes("Do you want to filter by date? "):
            date = prompt_filters_date()
            if date is not None:
                clauses.append(date)

    if len(clauses) == 0:
        log.error("No filters were specified")
        return None

    return " and ".join(clauses)

def filter_complaint(args):
    where = prompt_filters()
    if where is None:
        return ERROR

    attributes = [
        "complaint_id",
        "incident_id",
        "occurrence_date",
        "code",
        "organization",
        "description",
        "location_id",
        "city",
        "country"
    ]

    query = db.select("ComplaintView", where, attributes = attributes)

    if executeQuery(query) is None:
        log.error("Failed to execute filter query")
        return ERROR

    results = cursor.fetchall()
    if len(results) == 0:
        log.info("No results found")
        return SUCCESS

    headers = [tuple(attributes)]
    print_table(headers + results)
    return SUCCESS

def filter_crime(args):
    where = prompt_filters()
    if where is None:
        return ERROR

    attributes = [
        "crime_id",
        "incident_id",
        "occurrence_date",
        "code",
        "organization",
        "description",
        "location_id",
        "city",
        "country",
        "victim_id",
        "victim_first_name",
        "victim_last_name",
    ]

    query = db.select("CrimeView", where, attributes = attributes)

    if executeQuery(query) is None:
        log.error("Failed to execute filter query")
        return ERROR

    results = cursor.fetchall()
    if len(results) == 0:
        log.info("No results found")
        return SUCCESS

    headers =  [tuple(attributes)]
    print_table(headers + results)
    return SUCCESS

def filter_search(args):
    where = prompt_filters(code = False)
    if where is None:
        return ERROR

    attributes = [
        "search_id",
        "incident_id",
        "occurrence_date",
        "object",
        "location_id",
        "city",
        "country",
        "suspect_id",
        "suspect_first_name",
        "suspect_last_name",
    ]

    query = db.select("SearchView", where, attributes = attributes)

    if executeQuery(query) is None:
        log.error("Failed to execute filter query")
        return ERROR

    results = cursor.fetchall()
    if len(results) == 0:
        log.info("No results found")
        return SUCCESS

    headers =  [tuple(attributes)]
    print_table(headers + results)
    return SUCCESS

FILTER_HELP = {
    "complaint": "Filter complaint by location, date, and code",
    "crime":     "Filter crimes by location, date, and code",
    "search":    "Filter search by location and date",
    "help":      "Show this message",
}

def help_filter(args):
    log.info(f"{PROGRAM} filter complaint : {FILTER_HELP['complaint']}")
    log.info(f"{PROGRAM} filter crime     : {FILTER_HELP['crime']}")
    log.info(f"{PROGRAM} filter search    : {FILTER_HELP['search']}")
    log.info(f"{PROGRAM} filter help      : {FILTER_HELP['help']}")

def usage_filter():
    log.info(f"{PROGRAM} filter <command>")
    log.info(f"Try '{PROGRAM} filter help'")

FILTER_COMMANDS = {
    "complaint": filter_complaint,
    "crime":     filter_crime,
    "search":    filter_search,
    "help":      help_filter,
}

FILTER_MIN_ARGC = 0
FILTER_MAX_ARGC = 1

def filter(args):
    argc = len(args)
    if argc < FILTER_MIN_ARGC or argc > FILTER_MAX_ARGC:
        log.error("Incorrect number of arguments")
        usage_filter()
        return ERROR

    # default
    command = "help"
    if argc > 0:
        command = args[0]
    args = args[1:]

    if command not in FILTER_COMMANDS:
        log.error(f"Unknown command '{command}'")
        usage_filter()
        return ERROR

    return FILTER_COMMANDS[command](args)

# ===================== HELP ===================== #

HELP = {
    "help":         "Show this message",
    "create":       "Create all tables",
    "load":         "Load data from CSVs into tables",
    "clear":        "Delete all entries in tables",
    "clean":        "Drop all tables from database",
    "add":          "Add entries to the database",
    "delete":       "Delete entries from the database",
    "update":       "Update entries in the database",
    "background":   "Run background check on person",
    "show":         "Show detailed record information",
    "filter":       "Filter records by location, date, and code",
}

def help(args):
    log.info("=============================================")
    log.info(f"Usage: {PROGRAM} <command> [arguments]")
    log.info("=============================================")

    log.info(f"{PROGRAM} help                       : {HELP['help']}")
    log.info(f"{PROGRAM} create                     : {HELP['create']}")
    log.info(f"{PROGRAM} load [number_of_entries]   : {HELP['load']}")
    log.info(f"{PROGRAM} clear                      : {HELP['clear']}")
    log.info(f"{PROGRAM} clean                      : {HELP['clean']}")
    log.info(f"{PROGRAM} add                        : {HELP['add']}")
    log.info(f"{PROGRAM} delete                     : {HELP['delete']}")
    log.info(f"{PROGRAM} update                     : {HELP['update']}")
    log.info(f"{PROGRAM} background                 : {HELP['background']}")
    log.info(f"{PROGRAM} show                       : {HELP['show']}")
    log.info(f"{PROGRAM} filter                     : {HELP['filter']}")

    return SUCCESS

# ===================== CRIME ===================== #

COMMANDS = {
    "help":       help,
    "create":     create,
    "load":       load,
    "clean":      clean,
    "clear":      clear,
    "add":        add,
    "delete":     delete,
    "update":     update,
    "background": background,
    "show":       show,
    "filter":     filter
}

CRIME_MIN_ARGC = 1

def usage_crime():
    log.info(f"Usage: {PROGRAM} <command> [arguments]")
    log.info(f"Try '{PROGRAM} help'")
    return SUCCESS

def crime():
    argc = len(argv)

    if argc < CRIME_MIN_ARGC:
        log.error("Incorrect number of arguments")
        usage_crime()
        return ERROR

    # default
    command = "help"
    if argc > 1:
        command = argv[1]

    if command not in COMMANDS:
        log.error(f"Unknown command '{command}'")
        usage_crime()
        return ERROR

    args = argv[2:]
    return COMMANDS[command](args)

# ===================== MAIN ===================== #

def close(commit=False):
    if commit:
        connection.commit()

    closeDB(connection, cursor)

connection, cursor = connectDB()

if __name__ == '__main__':
    result = crime()
    commit = False
    if result == SUCCESS:
        commit = True

    close(commit)
    exit(result)
