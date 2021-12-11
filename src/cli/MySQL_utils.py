from configparser import ConfigParser
from getpass import getpass
from mysql.connector import connect, Error

DB_CONFIG_SECTION = 'mysqlconfig'

def getDatabaseConfig(config_file_path='config.ini'):
    config = ConfigParser()
    config.read(config_file_path)

    config_var_names = [
        'host',
        'user',
        'password',
        'database',
    ]

    config_vars = {}

    for var_name in config_var_names:
        var_value = config.get(DB_CONFIG_SECTION, var_name, fallback=None)

        if var_value is not None:
            config_vars[var_name] = var_value
        else:
            if var_name != 'password':
                config_vars[var_name] = input(f'{var_name}: ')
            else:
                config_vars[var_name] = getpass(f'{var_name}: ')

    return config_vars

def DQL(queries):
    results = []
    try:
        with connect(**getDatabaseConfig()) as connection:
            with connection.cursor() as cursor:
                for query in queries:
                    cursor.execute(query)
                    results.append(cursor.fetchall())
    except Error as e:
        print(e)

    return results