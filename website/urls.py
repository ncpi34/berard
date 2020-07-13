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
    path('deconnexion/', logout_view, name='logout'),

    url(r'accueil/$', ArticleView.as_view(), name='products'),
    path('groupe/<str:group>', ArticleView.as_view(model=Article), name='products_by_group'),
    path('groupe/<str:group>/famille/<str:family>', ArticleView.as_view(model=Article), name='products_by_family'),
    path('sous_famille/<str:subfamily>', ArticleView.as_view(model=Article), name='products_by_subfamily'),
    # path('home_by_family/<str:nom>', ArticleView.as_view(model=Article), name='products_by_sub_family'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='product_detail'),
    path('photo/<int:id>/', ArticlePictureView.as_view(), name='product_photo'),

    path('accueil_commande/', OrderSummaryView.as_view(), name='order_summary'),
    path('detail_commande/<int:pk>', OrderDetailView.as_view(), name='order_detail'),

    path('mot_de_passe_oublie/', ForgotPasswordView.as_view(), name='forgot_password'),
]
