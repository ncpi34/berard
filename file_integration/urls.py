from django.urls import path
from django.conf.urls import url
from .views import *


app_name = 'file'

urlpatterns = [
    path('', FileViews.index, name='login'),

]
