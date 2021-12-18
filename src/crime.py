import log
import os
import utils

from sys import argv

ADMIN = True   # Set this to false to restrict the CLI to user commands

INTERPRETER = "python3"
PROGRAM = os.path.basename(argv[0])

SUCCESS = 0
ERROR = -1

# ===================== USER COMMANDS ===================== #

HELP = {
    # USER COMMANDS #

    "help":     "Show this message",

    # ADMIN COMMANDS #

    "create":   "Create main and temporary database tables",
    "load":     "Load data from CSVs into temporary tables",
    "transfer": "Process and transfer data from temporary tables into main tables",
    "drop":     "Drop all temporary tables",
    "clean":    "Delete all entries in database tables",
    "clear":    "Drop all tables from database",
}

def help():
    log.info("---------------------------------------------")
    log.info(f"Usage: {INTERPRETER} {PROGRAM} <command> [arguments]")
    log.info("---------------------------------------------")

    if ADMIN:
        log.info(f"{INTERPRETER} {PROGRAM}   create               : {HELP['create']}")
        log.info(f"{INTERPRETER} {PROGRAM}     load               : {HELP['load']}")
        log.info(f"{INTERPRETER} {PROGRAM} transfer               : {HELP['transfer']}")
        log.info(f"{INTERPRETER} {PROGRAM}     drop               : {HELP['drop']}")
        log.info(f"{INTERPRETER} {PROGRAM}    clear               : {HELP['clear']}")
        log.info(f"{INTERPRETER} {PROGRAM}    clean               : {HELP['clean']}")

    log.info(f"{INTERPRETER} {PROGRAM}     help               : {HELP['help']}")
    log.info(f"{INTERPRETER} {PROGRAM}     foo  [arg_name(s)] : idk")

    return SUCCESS

# ===================== ADMIN COMMANDS ===================== #

def create():
    utils.runQueries("create.sql")

def load():
    utils.runQueries("load.sql")

def drop():
    utils.runQueries("drop.sql")

def transfer():
    log.note("Fix hacky transfer command")
    import transfer

def clean():
    utils.runQueries("clean.sql")

def clear():
    utils.runQueries("clear.sql")

# ===================== PROGRAM ===================== #

USER_COMMANDS = {
    "help": help,
}

ADMIN_COMMANDS = {
    "create":   create,
    "load":     load,
    "transfer": transfer,
    "drop":     drop,
    "clean":    clean,
    "clear":    clear,
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
