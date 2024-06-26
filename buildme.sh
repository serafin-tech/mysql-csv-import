#!/bin/bash

# set -x # only for DEBUGing
set -eu
set -o pipefail

NOCOLOR='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

function finish {
  echo -e "${RED}finished with some issue.${NOCOLOR}"
}

function echo_green {
  echo -e "${GREEN}$1${NOCOLOR}"
}

trap finish SIGINT SIGABRT SIGTERM

cd "$(dirname $0)"

if [[ ! -d venv ]]
then
  python3 -m venv venv
fi

rm -rf dist/ *.egg-info/ junit/ htmlcov/

source venv/bin/activate

python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt

python3 -m setuptools_scm

echo_green "================"
echo_green "=== BUILDING ==="
echo_green "================"

python3 -m build .

echo_green "==============="
echo_green "=== LINTING ==="
echo_green "==============="

pylint mysql_csv_import/ mysql-csv-import-cli.py

echo_green "==============="
echo_green "=== TESTING ==="
echo_green "==============="

pytest mysql_csv_import/tests/ \
  --doctest-modules \
  --junitxml=junit/test-results.xml \
  --cov=mysql_csv_import \
  --cov-report=xml --cov-report=html --cov-report=term
