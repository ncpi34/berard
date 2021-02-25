from django.urls import path
from file_integration.views.article import ArticleViews
from file_integration.views.client import ClientViews
from file_integration.views.family import FamilyViews
from file_integration.views.group import GroupViews
from file_integration.views.vat import VatViews
from file_integration.views.delete_article_non_unique import DeleteDoubleArticleViews
from file_integration.views.delete_cart_not_finalized import DeleteCartsViews
from file_integration.views.sub_family import SubFamilyViews

app_name = 'file'

urlpatterns = [
    # path('group/', GroupViews.create_group_csv, name='group_treatement'),
    # path('family/', FamilyViews.create_family, name='family_treatement'),
    # path('subfamily/', SubFamilyViews.create_sub_family, name='sub_family_treatement'),
    path('article/<password>/', ArticleViews.file_treatement, name='article_treatement'),
    path('vat/<password>/', VatViews.file_treatement, name='vat_treatement'),
    path('client/<password>/', ClientViews.file_treatement, name='client_treatement'),
    path('group/<password>/', GroupViews.create_group_and_others_xlsx, name='group_treatement'),

    path('non_unq/<password>/', DeleteDoubleArticleViews.file_treatement, name='non_unq'),
    path('del_carts/', DeleteCartsViews.file_treatement, name='del_carts'),

]
