#!/bin/bash

export DJANGO_SETTINGS_MODULE="ausgsteckt.settings.docker"

uv run python manage.py collectstatic --noinput
uv run python manage.py migrate
uv run gunicorn -b 0.0.0.0:8000 ausgsteckt.wsgi:application --workers 5 --log-level=info --log-file=-
