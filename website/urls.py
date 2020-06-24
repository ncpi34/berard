from django.urls import path
from . import views
from django.urls import path
from django.conf.urls import url
from .views import *
from django_filters.views import FilterView

app_name = 'website'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    # path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    url(r'home/$', (ArticleView.as_view()), name='products'),
    path('home_by_group/<str:group>', ArticleView.as_view(model=Article), name='products_by_group'),
    path('home_by_family/<str:family>', ArticleView.as_view(model=Article), name='products_by_family'),
    path('home_by_subfamily/<str:subfamily>', ArticleView.as_view(model=Article), name='products_by_subfamily'),
    # path('home_by_family/<str:nom>', ArticleView.as_view(model=Article), name='products_by_sub_family'),
    path('home_detail/<int:pk>', ArticleDetailView.as_view(), name='product_detail'),
    path('home_photo/<int:id>/', ArticleDetailView.as_view(), name='product_photo'),

    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('order_detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),

    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
]
