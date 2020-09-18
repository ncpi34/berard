from django.urls import path
from . import views
from django.urls import path
from django.conf.urls import url
from .views import *
from .pdf import PdfCreator
from django_filters.views import FilterView

app_name = 'order'

urlpatterns = [
    path('accueil_commande/', OrderSummaryView.as_view(), name='order_summary'),
    path('detail_commande/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('pdf/<order_id>', PdfCreator.build_pdf, name='generate_pdf'),
]
