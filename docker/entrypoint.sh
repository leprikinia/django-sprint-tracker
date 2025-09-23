#!/usr/bin/env bash
set -e

# Default values if not set
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"

# Run migrations + collectstatic on container start (idempotent)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start app server
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60
