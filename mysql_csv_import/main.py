#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-function-docstring,invalid-name

import argparse
import csv
import logging
from collections import namedtuple
from collections.abc import Iterator
from pathlib import PurePath
from pprint import pformat
from typing import Dict, List

import mysql.connector  # pylint: disable=import-error
from decouple import config  # pylint: disable=import-error


ArgParams = namedtuple('ArgParams',
                       {'verbose', 'file', 'database', 'table', 'host', 'port', 'user', 'password'})


def write_date_to_db(arg_params: ArgParams, col_headers: List[str], csv_data_iter: Iterator[List[Dict]]):
    try:
        cnx = mysql.connector.connect(user=arg_params.user,
                                      password=arg_params.password,
                                      host=arg_params.host,
                                      database=arg_params.database)

        add_query = (f"INSERT INTO {arg_params.table}({','.join(col_headers)}) "
                     f"VALUES({','.join(['%s'] * len(col_headers))})")
        logging.debug("query: %s", pformat(add_query))

        with cnx.cursor() as cursor:
            try:
                for csv_data in csv_data_iter:
                    logging.debug("loading chunk size: %d", len(csv_data))
                    cursor.executemany(add_query, [list(row.values()) for row in csv_data])

                cnx.commit()

            except mysql.connector.Error as exception:
                logging.info("error: %s", str(exception))
            else:
                logging.info("data loaded successfully.")

        cnx.close()

    except mysql.connector.Error as err:
        logging.error("database operation error: %s", str(err))
        raise


def read_csv_file_iterator(file: str, batch_size: int = 512) -> Iterator[List[Dict]]:
    try:
        with open(file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            ret_list = []
            for row in reader:
                ret_list.append(row)

                if len(ret_list) >= batch_size:
                    yield ret_list
                    ret_list = []

            yield ret_list

    except FileNotFoundError as exception:
        logging.error("File not found: %s, details: %s", file, str(exception))
        raise

    except csv.Error as exception:
        logging.error("Reading error for file: %s, details: %s", file, str(exception))
        raise


def read_csv_file_headers(file: str) -> List[str]:
    try:
        with open(file, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            return next(reader)

    except FileNotFoundError as exception:
        logging.error("File not found: %s, details: %s", file, str(exception))
        raise

    except csv.Error as exception:
        logging.error("Reading error for file: %s, details: %s", file, str(exception))
        raise


def args_parser(args_list: list[str]):
    db_user = config('DB_USER', default=None)
    db_pass = config('DB_PASS', default=None)
    db_host = config('DB_HOST', default='127.0.0.1')
    db_port = config('DB_PORT', default=3306, cast=int)

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
                        default=db_host)

    parser.add_argument('-P', '--port',
                        help='database port, default 3306, read from .env from DB_PORT',
                        default=db_port,
                        type=int)

    parser.add_argument('-u', '--user',
                        help='username for database connection, read from .env from DB_USER',
                        default=db_user)

    parser.add_argument('-p', '--password',
                        help='password for database connection, read from .env from DB_PASS',
                        default=db_pass)

    params = parser.parse_args(args=args_list)

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
    arg_params = args_parser(None)

    logging_setup(arg_params.verbose)

    logging.debug("arguments: %s", pformat(arg_params))

    csv_headers = read_csv_file_headers(file=arg_params.file)
    logging.debug("csv headers: %s", pformat(csv_headers))

    write_date_to_db(arg_params, csv_headers, read_csv_file_iterator(file=arg_params.file))


if __name__ == '__main__':
    main()
