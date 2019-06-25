#!/bin/bash

RUNUSER="${RUN_AS_USER:-1000:1000}"
RUN="chroot --userspec=$RUNUSER --skip-chdir /"

# start broker
rabbitmq-server -detached

# make sure database is readable
chown -f $RUNUSER renamer.sqlite3

# start celery
$RUN python manage.py celery worker --logfile=/opt/tmp/renamer-worker.log --loglevel=INFO --time-limit=3600 --concurrency=2 &

# start Django
exec gunicorn --user=1000 --bind=:8000 renamer.wsgi:application 
