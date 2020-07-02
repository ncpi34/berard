from celery import shared_task, states, task
from celery.schedules import crontab
from django.core.management import call_command
import requests
from celery.utils.log import get_task_logger
from file_integration.views.client_without_route import ClientAutomate
from file_integration.views.article_without_route import ArticleAutomate

logger = get_task_logger(__name__)


@shared_task()
def upload_clients_task():  # clients
    print('start client task')
    response = ClientAutomate.file_treatement()
    print(response)
    # response = requests.get(url='http://127.0.0.1:8000/file/client')
    # print('waiting response')
    # print(response)
    return '{}'.format('done')


@shared_task()
def upload_articles_task():  # articles
    print('start article task')
    response = ArticleAutomate.file_treatement()
    print(response)
    # response = requests.get(url='http://127.0.0.1:8000/file/article')
    # print('waiting response')
    # print(response)
    return '{}'.format('done')
