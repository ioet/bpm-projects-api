#!/usr/bin/env bash

for pkg in "$@"
do
    echo "Installing '$pkg'"
    pip install ${pkg}
done
pip freeze > requirements.txt && echo "requirements.txt updated successfully"