from django.urls import path
from . import views
from django.urls import path
from django.conf.urls import url
from .views import *
from django_filters.views import FilterView

app_name = 'website'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('deconnexion/', logout_view, name='logout'),
    path('mot_de_passe_oublie/', ForgotPasswordView.as_view(), name='forgot_password'),

    path('accueil/', HomeView.as_view(), name='home'),

    url(r'produit/$', ArticleView.as_view(), name='products'),
    path('groupe/<int:group>/', ArticleView.as_view(model=Article), name='products_by_group'),
    path('groupe/<int:group>/famille/<int:family>/', ArticleView.as_view(model=Article), name='products_by_family'),
    path('groupe/<int:group>/famille/<int:family>/sous_famille/<int:subfamily>', ArticleView.as_view(model=Article), name='products_by_subfamily'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='product_detail'),

    path('offres/', OffersView.as_view(), name='offers'),
    path('favoris/', FavoritesView.as_view(), name='favorites'),

]
