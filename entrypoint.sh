#!/bin/bash
APP_PORT=${PORT:-8000}
cd /app/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm form.wsgi:application --bind "0.0.0.0:${APP_PORT}"

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"andinidev93@gmail.com"}
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --email $DJANGO_SUPERUSER_EMAIL --noinput || true