from django.urls import path
from django.conf.urls import url
from .views import *


app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('update/<int:product_id>/', cart_update, name='cart_update'),
    path('update_all_cart/', update_all_cart, name='update_all_cart'),
    # path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('cart_remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('send_order/', SendOrderView.as_view(), name='send_order'),
    # path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    # path('cart/item_increment/<int:id>/',
    #      views.item_increment, name='item_increment'),
    # path('cart/item_decrement/<int:id>/',
    #      views.item_decrement, name='item_decrement'),
]


