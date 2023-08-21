#!/bin/bash

cd python

if [ -z "$(find . -name '*.py')" ]; then
  echo "No Python files found. Skipping build and test."
  exit 0
fi

python -m pip install --upgrade pip
pip install ruff pytest
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# stop the build if there are Python syntax errors or undefined names
ruff --format=github --select=E9,F63,F7,F82 --target-version=py37 .
# default set of ruff rules with GitHub Annotations
ruff --format=github --target-version=py37 .

pytest
