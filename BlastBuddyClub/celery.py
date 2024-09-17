import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'BlastBuddyClub.settings')

app = Celery('BlastBuddyClub', broker=os.getenv('APP_BROKER_URI'))

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# # this would require investigation weather or not this should be used.
# # Load task modules from all registered Django apps.
app.autodiscover_tasks()
