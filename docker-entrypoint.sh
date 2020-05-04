#!/bin/bash

RUNUSER="${RUN_AS_USER:-1000}"
RUNGROUP="${RUN_AS_GROUP:-1000}"
RUN="chroot --userspec=$RUNUSER:$RUNGROUP --skip-chdir /"

# start celery
$RUN python manage.py celery worker --logfile=$APP_TMPDIR/renamer-worker.log --loglevel=INFO --time-limit=3600 --concurrency=2 &

# start Django
exec gunicorn --user=$RUNUSER --bind=:8000 --timeout=120 --log-file=- --log-level=DEBUG renamer.wsgi:application
