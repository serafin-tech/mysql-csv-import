#!/usr/bin/env python3

import argparse
import csv
import logging
from collections import namedtuple
from pathlib import PurePath
from pprint import pformat
from typing import Dict, List

import mysql.connector as db_connector
# import mariadb as db_connector
from decouple import config


ArgParams = namedtuple('ArgParams',
                       {'verbose', 'file', 'database', 'table', 'host', 'port', 'user', 'password'})


def write_date_to_db(arg_params: ArgParams, csv_data: List[Dict]):
    try:
        cnx = db_connector.connect(user=arg_params.user,
                                   password=arg_params.password,
                                   host=arg_params.host,
                                   database=arg_params.database)

        add_query = (f"INSERT INTO {arg_params.table}({','.join(csv_data[0].keys())}) "
                     f"VALUES({','.join(['%s'] * len(csv_data[0].keys()))})")
        logging.debug("query: %s", pformat(add_query))

        with cnx.cursor() as cursor:
            cursor.executemany(add_query, [list(row.values()) for row in csv_data])

        cnx.commit()
        cnx.close()

    except db_connector.Error as err:
        logging.error("database operation error: %s", str(err))
        raise


def read_csv_file(file: str) -> List[Dict]:
    try:
        with open(file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            ret = list()
            for row in reader:
                ret.append(row)

    except FileNotFoundError as err:
        logging.error("File not found: %s", file)
        raise

    except csv.Error as err:
        logging.error("Reading error for file: %s", file)
        raise

    return ret


def args_parser():
    DB_USER = config('DB_USER', default=None)
    DB_PASS = config('DB_PASS', default=None)
    DB_HOST = config('DB_HOST', default='127.0.0.1')
    DB_PORT = config('DB_PORT', default=3306, cast=int)

    parser = argparse.ArgumentParser(description='Importing CSV data into MySQL database')

    parser.add_argument('-v', '--verbose',
                        help='talkative mode',
                        action='store_true',
                        default=False)

    parser.add_argument('-f', '--file',
                        help='file to import data from',
                        required=True)

    parser.add_argument('-D', '--database',
                        help='database to import data to',
                        required=True)

    parser.add_argument('-t', '--table',
                        help='table to import data to, if not provided taken from file name')

    parser.add_argument('-H', '--host',
                        help='database host, default 127.0.0.1, read from .env from DB_HOST',
                        default=DB_HOST)

    parser.add_argument('-P', '--port',
                        help='database port, default 3306, read from .env from DB_PORT',
                        default=DB_PORT)

    parser.add_argument('-u', '--user',
                        help='username for database connection, read from .env from DB_USER',
                        default=DB_USER)

    parser.add_argument('-p', '--password',
                        help='password for database connection, read from .env from DB_PASS',
                        default=DB_PASS)

    params = parser.parse_args()

    return ArgParams(verbose=params.verbose,
                     file=params.file,
                     database=params.database,
                     table=params.table if params.table else PurePath(params.file).stem,
                     host=params.host,
                     port=params.port,
                     user=params.user,
                     password=params.password)


def logging_setup(verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def main():
    arg_params = args_parser()

    logging_setup(arg_params.verbose)

    logging.debug("arguments: %s", pformat(arg_params))

    csv_data = read_csv_file(file=arg_params.file)
    logging.debug("csv_data: %s", pformat(csv_data))

    write_date_to_db(arg_params, csv_data)


if __name__ == '__main__':
    main()
