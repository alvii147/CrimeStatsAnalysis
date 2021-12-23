# Crime Stats Analysis

This project involves the collection of crime records datasets from law enforcement departments in UK and US, and the process of developing an optimally designed database and a client interface for the definition, manipulation and storage of this data. Please see the [report](https://alvii147.github.io/CrimeStatsAnalysis/report/Report) or the [video presentation](https://youtu.be/aTREWcHJalw) for more information.

## Installation

Clone the repository:

```bash
git clone https://github.com/alvii147/CrimeStatsAnalysis.git
```

Navigate into repository directory:

```bash
cd CrimeStatsAnalysis/
```

Create and activate Python virtual environment (optional):

```bash
python3 -m venv env
# Linux & MacOS
source env/bin/activate
# Windows
source env/Scripts/activate
```

Install dependencies:

```bash
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

> :warning: **Warning**
>
> Storing the password in the configuration file is NOT recommended. Currently, the `.gitignore` is written to ignore the configuration file when committing to version control system. However, this is not completely fool-proof as the configuration file may be committed accidentally if the `.gitignore` is missing or renamed.

## Command-Line Interface

Once the installation and configuration are complete, run the `crime.py` python script (while inside the virtual environment) to create the appropriate tables, load the data and transfer the data into the right tables:

```bash
cd src/
python3 crime.py
```

<img alt="Secret Ingredient Meme" src="docs/img/secret_ingredient.png" width="600" />
