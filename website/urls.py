from django.urls import path
from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='index'),
    path('logout/', logout_view, name='logout'),
    path('home/', ArticleView.as_view(template_name='home.html'), name='home'),
]