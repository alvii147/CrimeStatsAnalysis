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
    config_vars : dict
        Dictionary containing the host name, username, password and
        database name.
    '''

    # parse config file
    config = ConfigParser()
    config.read(path)

    config_var_names = [
        'host',
        'user',
        'password',
        'database',
    ]

    config_vars = {}

    for var_name in config_var_names:
        # get config variables from config file
        var_value = config.get(sec, var_name, fallback=None)

        if var_value is None:
            # if config variable not found, prompt for it using stdin
            if var_name == 'password':
                # if password config variable, get stdin without echo
                config_vars[var_name] = getpass(f'{var_name}: ')
            else:
                config_vars[var_name] = input(f'{var_name}: ')
        else:
            # if password config variable found, throw warning
            if var_name == 'password':
                warnings.warn(
                    'Storing plain text format password in config file ' \
                    'is not recommended.'
                )

            config_vars[var_name] = var_value

    return config_vars

def connectDB(operation):
    '''
    Establish MySQL connection and execute given operation

    Parameters
    ----------
    operation : callable
        Callable to execute with ``connection`` and ``cursor`` objects.

    Returns
    -------
    output
        Output of executed ``operation``
    '''

    output = []
    # connect to database
    with connect(**configDB()) as connection:
        with connection.cursor() as cursor:
            # run given operation
            output = operation(
                connection=connection,
                cursor=cursor,
            )

    return output