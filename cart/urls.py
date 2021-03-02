from django.urls import path
from django.conf.urls import url
from .views import *
from django.urls import reverse


app_name = 'cart'

urlpatterns = [
    # <path:encoded_url>
    path('', cart_detail, name='cart_detail'),

    path('add/<product_id>/', cart_add, name='cart_add'),
    path('add_order_summary_to_cart/<order_id>/', order_summary_to_cart, name='order_summary_to_cart'),

    path('update/<product_id>/', cart_update, name='cart_update'),
    path('update_all_cart/', update_all_cart, name='update_all_cart'),

    path('cart_remove/<str:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('send_order/', SendOrderView.as_view(), name='send_order'),

]
