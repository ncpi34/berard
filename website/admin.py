from django.contrib import admin
from django.contrib.auth.models import Group
from website.models import ProfilUtilisateur, Article
from django.contrib.auth.models import User

"""Admin Part"""
admin.site.unregister(Group)
admin.site.register(ProfilUtilisateur)
admin.site.register(Article)
