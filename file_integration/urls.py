from django.urls import path
from file_integration.views.article import ArticleViews
from file_integration.views.client import ClientViews

app_name = 'file'

urlpatterns = [
    path('article/', ArticleViews.file_treatement, name='article_treatement'),
    path('client/', ClientViews.file_treatement, name='article_treatement'),

]
