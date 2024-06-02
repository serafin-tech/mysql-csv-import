# pylint: disable=missing-function-docstring,missing-module-docstring

import os
import shlex

import pytest

from mysql_csv_import.main import read_csv_file, args_parser

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.parametrize("file_name, expected_data", [(
        f"{TESTS_DIR}/data/test.csv", [{
            'col_char': 'łańcuch znaków',
            'col_int': '1',
            'col_date': '2023-12-14',
        }, {
            'col_char': 'inny łańcuch znaków',
            'col_int': '2',
            'col_date': '2024-01-01',
        }]
)])
def test_read_csv_file(file_name, expected_data):
    read_data = read_csv_file(file_name)
    assert read_data == expected_data


@pytest.mark.parametrize("payload, expected_data", [(
        '--verbose ' # beware spaces as last character
        '--file file_name.csv '
        '--database database_name '
        '--table table_name '
        '--host host_name '
        '--port 3306 '
        '--user user_name '
        '--password password_value',
        [
            ('verbose', True),
            ('file', 'file_name.csv'),
            ('database', 'database_name'),
            ('table', 'table_name'),
            ('host', 'host_name'),
            ('port', 3306),
            ('user', 'user_name'),
            ('password', 'password_value')
        ]
)])
def test_args_parser(payload, expected_data):
    params_dict = args_parser(shlex.split(payload))._asdict()

    assert all(params_dict[field] == value for field, value in expected_data)
