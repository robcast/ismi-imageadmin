import djcelery

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

ARCHIVE_LOCATION = "/Users/ahankins/Documents/code/git/renamer/testing/data1"
INCOMING_LOCATION = "/Users/ahankins/Documents/code/git/renamer/testing/data3/incoming"
DIVA_LOCATION = "/Users/ahankins/Documents/code/git/renamer/testing/data7/srv/images"

PATH_TO_GS = "/usr/local/bin/gs"
PATH_TO_VIPS = "/usr/local/bin/vips"
PATH_TO_SHASUM = "/usr/bin/shasum"


djcelery.setup_loader()
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "ISMI"
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

CELERY_RESULT_BACKEND = "database"
#Note: If youre using SQLite as the Django database backend, celeryd will only be able to process one task at a time,
#this is because SQLite doesnt allow concurrent writes.
CELERY_RESULT_DBURI = "sqlite:///db.sqlite"