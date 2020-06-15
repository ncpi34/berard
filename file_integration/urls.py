from django.urls import path
from file_integration.views.article import ArticleViews
from file_integration.views.client import ClientViews
from file_integration.views.family import FamilyViews
from file_integration.views.group import GroupViews
from file_integration.views.sub_family import SubFamilyViews

app_name = 'file'

urlpatterns = [
    path('article/', ArticleViews.file_treatement, name='article_treatement'),
    path('client/', ClientViews.file_treatement, name='client_treatement'),
    # path('group/', GroupViews.create_group_csv, name='group_treatement'),
    # path('family/', FamilyViews.create_family, name='family_treatement'),
    # path('subfamily/', SubFamilyViews.create_sub_family, name='sub_family_treatement'),
    path('group/', GroupViews.create_group_and_others_xlsx, name='group_treatement'),

]
