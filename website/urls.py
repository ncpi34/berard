from django.urls import path
from . import views
from django.urls import path
from django.conf.urls import url
from .views import *
from django_filters.views import FilterView

app_name = 'website'

urlpatterns = [
    path('', login_view, name='index'),
    path('logout/', logout_view, name='logout'),

    path('home/', ArticleView.as_view(model=Article), name='products'),
    path('<str:nom>/home/', ArticleView.as_view(model=Article), name='products_by_familly'),
    path('<int:pk>/home/', ArticleDetailView.as_view(), name='product_detail'),

]
