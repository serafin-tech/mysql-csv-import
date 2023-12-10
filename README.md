# mysql-csv-import

CLI tool for importing data from CSV file into MySQL/MariaDB table

```shell
usage: mysql-csv-import.py [-h] [-v] -f FILE -D DATABASE [-t TABLE] [-H HOST] [-P PORT] [-u USER] [-p PASSWORD]

Importing CSV data into MySQL database

options:
  -h, --help            show this help message and exit
  -v, --verbose         talkative mode
  -f FILE, --file FILE  file to import data from
  -D DATABASE, --database DATABASE
                        database to import data to
  -t TABLE, --table TABLE
                        table to import data to, if not provided taken from file name
  -H HOST, --host HOST  database host, default 127.0.0.1, read from .env from DB_HOST
  -P PORT, --port PORT  database port, default 3306, read from .env from DB_PORT
  -u USER, --user USER  username for database connection, read from .env from DB_USER
  -p PASSWORD, --password PASSWORD
                        password for database connection, read from .env from DB_PASS
```

## CSV file format required

1. first row of the file shall contain column headers
2. following rows shall contain data, number of cells shall be equal to number of column headers

sample file:

```csv
col_char,col_int,col_date
string,1,2023-12-14
characters,2,2024-01-01
```