import djcelery

FORCE_SCRIPT_NAME = "/"

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'renamer.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# ARCHIVE_LOCATION = "/Users/ahankins/Documents/code/git/renamer/testing/data1"
# INCOMING_LOCATION = "/Users/ahankins/Documents/code/git/renamer/testing/data3/incoming"
# DIVA_LOCATION = "/Users/ahankins/Documents/code/git/renamer/testing/data7/srv/images"
# TMPDIR = "/Users/ahankins/.tmp"
ARCHIVE_LOCATION = "/tusi/data1"
INCOMING_LOCATION = "/tusi/data3/incoming"
DIVA_LOCATION = "/tusi/data7/srv/images"
DATA_LOCATION = "/tusi/data7/srv/data"
BACKUP_LOCATION = "/tusi/data3/backup"
TMPDIR = "/var/tmp"


PATH_TO_GS = "/usr/bin/gs"
PATH_TO_VIPS = "/usr/bin/vips"
PATH_TO_SHASUM = "/usr/bin/shasum"
PATH_TO_KDU = "/usr/local/bin/kdu_compress"


djcelery.setup_loader()
CELERY_IMPORTS = ("renamer.helpers.to_archive",
                  "renamer.helpers.to_diva",
                  "renamer.helpers.generate_json")
#BROKER_URL = "amqp://guest@localhost:5672//"
BROKER_URL = 'django://'
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

CELERY_RESULT_BACKEND = "database"
#Note: If youre using SQLite as the Django database backend, celeryd will only be able to process one task at a time,
#this is because SQLite doesnt allow concurrent writes.
CELERY_RESULT_DBURI = "sqlite:///db.sqlite"
