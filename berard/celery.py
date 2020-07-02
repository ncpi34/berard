from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery import shared_task, states, task
from django.core.management import call_command
import requests
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'berard.settings')
app = Celery('berard')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.update(
#     # task_serializer='json',
#     # accept_content=['json'],  # Ignore other content
#     # result_serializer='json',
#     # result_expires=36000,
#     enable_utc=True,
#     timezone='Europe/Paris',
# )

app.conf.beat_schedule = {
    "every day client update": {
        "task": "file_integration.tasks.upload_clients_task",  # <---- Name of task
        # 'schedule': 60.0,
        "schedule": crontab(hour=9,
                            minute=30)
    },
    "every day article update": {
        "task": "file_integration.tasks.upload_articles_task",  # <---- Name of task
        # 'schedule': 60.0,
        "schedule": crontab(hour=9,
                            minute=20)
    },
    # "every minute": {
    #     "task": "berard.tasks.upload_clients_task",
    #     'schedule': 10.0,
    # }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
