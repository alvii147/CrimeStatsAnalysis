# Crime Stats Analysis

## Installation

```bash
# clone repository
git clone https://github.com/alvii147/CrimeStatsAnalysis.git
# navigate into cloned repository
cd CrimeStatsAnalysis/
```

```bash
# create python virtual environment
python3 -m venv env
# activate virtual environment
source env/bin/activate
# install dependencies
pip3 install -r requirements.txt
```

## Configuration

Store configuration data into file `src/MySQLutils/config.ini`:

```bash
echo [mysqlconfig] > src/MySQLutils/config.ini
echo host = <hostname> >> src/MySQLutils/config.ini
echo user = <username> >> src/MySQLutils/config.ini
echo password = <password> >> src/MySQLutils/config.ini
echo database = <databasename> >> src/MySQLutils/config.ini
```

For `<hostname>` use the hostname of the database, for eg. `marmoset04.shoshin.uwaterloo.ca`.

For `<username>` and `<password>` use your MySQL username and password.

For `<databasename>` use the name of your database.

`config.ini` should then look something like this:

```ini
[mysqlconfig]
host = marmoset04.shoshin.uwaterloo.ca
user = waterlooid
password = mylittlepony
database = db356_waterlooid
```

Storing configuration in file is optional, and if not done, the program will continuously prompt for user input every time a database connection is attempted for every missing configuration variable.

> **WARNING**
>
> Storing the password in the configuration file is NOT recommended. Currently, the `.gitignore` is written to ignore the configuration file when committing to version control system. However, this is not completely fool-proof as the configuration file may be committed accidentally if the `.gitignore` is missing or renamed.

## Command-Line Interface

Once the installation and configuration are complete, run the `crime.py` python script (while inside the virtual environment) to create the appropriate tables, load the data and transfer the data into the right tables:

```bash
cd src/
python3 crime.py
```

**NOTE:** You must set `ADMIN` to `True` inside the script to gain access to the database creation commands

<img alt="Secret Ingredient Meme" src="docs/img/secret_ingredient.png" width="600" />
