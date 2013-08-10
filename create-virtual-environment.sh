#!/bin/bash

if [ -d venv ]; then
    echo "Delete venv and create new [n] or simply update packages [U]?"
    read answer
    if [ "$answer" == "n" ]; then
        rm -rf venv
        virtualenv --no-site-packages venv
    elif [ "$answer" != "U" -a "$answer" != "" ]; then
        echo "Invalid input"
        exit
    fi
else
    virtualenv --no-site-packages venv
fi
./venv/bin/pip install -r etc/requirements.txt --upgrade

