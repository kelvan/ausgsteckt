#!/bin/bash

# wait for postgres
POSTGRES=$(echo ${DATABASE_URL} | sed -E 's/.*@([^:]+):([0-9]+).*/\1:\2/')
wait-for-it -t 0 ${POSTGRES}

python manage.py migrate
gunicorn -b 0.0.0.0:8000 ausgsteckt.wsgi:application --workers 5 --log-level=info --log-file=-
