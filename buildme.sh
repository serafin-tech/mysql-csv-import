#!/bin/bash

if [[ ! -d venv ]]
then
  python3.11 -m venv venv
fi

source venv/bin/activate

python3.11 -m pip install -U pip
python3.11 -m pip install -r requirements.txt

python3 -m pip install -U build setuptools setuptools-scm

rm -rf dist/ *.egg-info/

python3 -m setuptools_scm

python3 -m build .
