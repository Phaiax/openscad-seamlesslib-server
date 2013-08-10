#!/bin/bash

./venv/bin/python src/manage.py test --settings=seamless.settings_test "$@"
