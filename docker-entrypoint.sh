#!/bin/bash

# start celery
python manage.py celery worker --logfile=/opt/tmp/renamer-worker.log --loglevel=INFO --time-limit=3600 --concurrency=2 &

# start Django
exec gunicorn renamer.wsgi:application --bind=:8000
