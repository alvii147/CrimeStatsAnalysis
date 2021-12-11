# Crime Stats Analysis

<img alt="Secret Ingredient Meme" src="img/secret_ingredient.png" width="600" />

## Command-Line Interface

*under construction*

### Installation

```bash
# create virtual environment
python3 -m venv env
# activate virtual environment
source env/bin/activate
# install mysql python connector
pip3 install mysql-connector-python
```

### Configuration

Create file `config.ini` in `src/cli/` and edit it:

```ini
[mysqlconfig]
host = <hostname>
user = <username>
password = <password>
database = <databasename>
```

### Run Queries

```bash
python3
```

```python
>>> from MySQL_utils import RunQuery
>>>
>>> queries = ['SHOW TABLES;', 'DESCRIBE Incident']
>>> output = RunQuery(queries)
>>> _ = [print(row[0]) for row in output[0]]
Code
Complaint
Crime
Incident
Location
Person
Search
>>> _ = [print(row[0], row[1]) for row in output[1]]
incident_id b'int'
location_id b'int'
occurence_date b'date'
type b'varchar(128)'
```