#!/bin/bash
set -e

echo "Starting management."
poetry run python manage.py migrate --noinput
poetry run python manage.py runserver 0.0.0.0:5050
