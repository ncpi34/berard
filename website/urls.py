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

    # url(r'^home/$', ArticleView.as_view(model=Article), name='home'),
    # path('home_filter/<str:name>', ArticleFiltersView.as_view(model=Article), name='home_filter'),
    path('home/', ArticleView.as_view(model=Article), name='products'),
    path('<str:nom>/home/', ArticleFiltersView.as_view(model=Article), name='products_by_familly'),
    # path('<int:id>/home/', ArticleFiltersView.as_view(model=Article), name='product_details'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
]