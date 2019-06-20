#!/bin/bash

# start Django
python manage.py runserver --traceback 0.0.0.0:8000 2>&1 >/opt/tmp/renamer-django.log &

# start celery
python manage.py celery worker --logfile=/opt/tmp/renamer-worker.log --loglevel=INFO --time-limit=3600 --concurrency=2 &

# wait
tail -f /dev/null
