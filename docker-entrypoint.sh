#!/bin/bash

until pg_isready --host db; do
    echo 'Waiting for PostgreSQL to become available...'
    sleep 1
done
echo 'PostgreSQL is available'

# create user for celery worker
addgroup --gid "${RUN_AS_GROUP:-1000}" worker
adduser --system --uid "${RUN_AS_USER:-1000}" --gid "${RUN_AS_GROUP:-1000}" --disabled-password worker
# start celery worker
celery -A renamer worker --uid worker --logfile=$APP_TMPDIR/renamer-worker.log --loglevel="${RUN_LOG_LEVEL:-INFO}" --time-limit=3600 --concurrency=2 &

if [ "${RUN_MODE}" == "development" ] ; then
    # Django dev server
    exec python manage.py runserver 0:8000
else
    # start Django
    exec gunicorn --user=worker --bind=:8000 --timeout=420 --log-file=- --log-level=DEBUG renamer.wsgi:application
fi
