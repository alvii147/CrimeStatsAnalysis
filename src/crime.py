import log
import os
import utils
import transfer

from sys import argv

ADMIN = True   # Set this to false to restrict the CLI to user commands

INTERPRETER = "python3"
PROGRAM = os.path.basename(argv[0])

SUCCESS = 0
ERROR = -1

# ===================== USER COMMANDS ===================== #

HELP = {
    # USER COMMANDS #

    "help": "Show this message",

    # ADMIN COMMANDS #

    "create": "Create all tables",
    "load":   "Load data from CSVs into tables",
    "clear":  "Delete all entries in tables",
    "clean":  "Drop all tables from database",
}

def help():
    log.info("--------------------------------------------------------------------------------")
    log.info(f"Usage: {INTERPRETER} {PROGRAM} <command> [arguments]")
    log.info("--------------------------------------------------------------------------------")

    if ADMIN:
        log.info(f"{INTERPRETER} {PROGRAM} create : {HELP['create']}")
        log.info(f"{INTERPRETER} {PROGRAM} load   : {HELP['load']}")
        log.info(f"{INTERPRETER} {PROGRAM} clear  : {HELP['clear']}")
        log.info(f"{INTERPRETER} {PROGRAM} clean  : {HELP['clean']}")

    log.info(f"{INTERPRETER} {PROGRAM} help   : {HELP['help']}")

    log.info("--------------------------------------------------------------------------------")

    return SUCCESS

# ===================== ADMIN COMMANDS ===================== #

def create():
    utils.runQueries("SQL/create.sql")
    utils.runQueries("SQL/keys.sql")
    utils.runQueries("SQL/views.sql")

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

# ===================== PROGRAM ===================== #

USER_COMMANDS = {
    "help": help,
}

ADMIN_COMMANDS = {
    "create": create,
    "load":   load,
    "clean":  clean,
    "clear":  clear,
}

COMMANDS = USER_COMMANDS
if ADMIN:
    COMMANDS.update(ADMIN_COMMANDS)

MIN_ARGS = 1
MAX_ARGS = 2

def usage():
    log.info(f"Usage: {INTERPRETER} {PROGRAM} <command> [arguments]")
    log.info(f"Try: {INTERPRETER} {PROGRAM} help")
    return SUCCESS

argc = len(argv)

if argc < MIN_ARGS or argc > MAX_ARGS:
    log.error("Incorrect number of arguments")
    usage()
    exit(ERROR)

if argc == 1:
    command = "help"
else:
    command = argv[1]

if command not in COMMANDS:
    log.error(f"Unknown commmand '{command}'")
    usage()
    exit(ERROR)

exit(COMMANDS[command]())
