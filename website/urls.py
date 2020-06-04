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

    # path('home/', ArticleView.as_view(model=Article), name='products'),
    url(r'home/$', ArticleView.as_view(), name='products'),
    path('<str:nom>/home/', ArticleView.as_view(model=Article), name='products_by_familly'),
    path('home_detail/<int:pk>', ArticleDetailView.as_view(), name='product_detail'),

    path('<int:id>/home/', ArticleDetailView.as_view(), name='display_modal'),

]
