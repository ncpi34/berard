from django.urls import path
from . import views
from django.urls import path
from django.conf.urls import url
from .views import *
from django_filters.views import FilterView

app_name = 'website'

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    url(r'home/$', ArticleView.as_view(), name='products'),
    path('home_by_familly/<str:nom>', ArticleView.as_view(model=Article), name='products_by_familly'),
    path('home_detail/<int:pk>', ArticleDetailView.as_view(), name='product_detail'),
    path('home_photo/<int:id>/', ArticleDetailView.as_view(), name='product_photo'),

    path('history/', HistoryView.as_view(), name='history'),
]
