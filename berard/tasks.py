from celery import shared_task, states, task
from celery.schedules import crontab
from django.core.management import call_command
import requests
from celery.utils.log import get_task_logger

# logger = get_task_logger(__name__)


@shared_task(run_every=crontab(minute=1))
def upload_clients_task():
    print('eeeeeeeeeeeeeeee')
    # do something
    # response = requests.get(url='http://127.0.0.1:8000/file/client')
    # print(response)
    return '{}'.format('eeeeeeeeeeee')
