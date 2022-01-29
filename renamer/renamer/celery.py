import os

from celery import Celery
from celery.signals import setup_logging

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'renamer.settings')

app = Celery('renamer')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    # parse Django logging config
    dictConfig(settings.LOGGING)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
