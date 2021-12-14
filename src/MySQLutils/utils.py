from getpass import getpass
from pathlib import Path
from configparser import ConfigParser
import warnings
from mysql.connector import connect

def configDB(path=Path(__file__).parent / 'config.ini', sec='mysqlconfig'):
    '''
    Parse config file and get user input for database configuration
    variables.

    Parameters
    ----------
    config_file_path : str or ``pathlib.Path`` object
        Path to config file as string or ``pathlib.Path`` object.
    config_section : str
        Section name in config file that contains database configuration.

    Returns
    -------
    config : dict
        Dictionary containing the host name, username, password and
        database name.
    '''

    # parse config file
    parser = ConfigParser()
    parser.read(path)

    config_var_names = [
        'host',
        'user',
        'password',
        'database',
    ]

    config = {}

    for var_name in config_var_names:
        # get config variables from config file
        var_value = parser.get(sec, var_name, fallback=None)

        if var_value is None:
            # if config variable not found, prompt for it using stdin
            if var_name == 'password':
                # if password config variable, get stdin without echo
                config[var_name] = getpass(f'{var_name}: ')
            else:
                config[var_name] = input(f'{var_name}: ')
        else:
            # if password config variable found, throw warning
            if var_name == 'password':
                warnings.warn(
                    'Storing plain text format password in config file ' \
                    'is not recommended.'
                )

            config[var_name] = var_value

    return config

def connectDB(config=None):
    '''
    Establish MySQL database connection.

    Parameters
    ----------
    config : dict, optional

    Returns
    -------
    connection : MySQLConnection
        ``MySQLConnection`` object of created connection.
    cursor : MySQLCursor
        ``MySQLCursor`` object of created connection.
    '''

    # get database configuration
    if config is None:
        config = configDB()

    # connect to database
    connection = connect(**config)
    cursor = connection.cursor()

    return connection, cursor

def closeDB(connection, cursor):
    '''
    Close MySQL database connection.

    Parameters
    ----------
    connection : MySQLConnection
        ``MySQLConnection`` object of connection to close.
    cursor : MySQLCursor
        ``MySQLCursor`` object of connection to close.
    '''

    # close cursor
    cursor.close()
    # close connection
    connection.close()