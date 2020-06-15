from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from website.models import ProfilUtilisateur, Article, Historique
from django.db.models import ManyToOneRel, ForeignKey, OneToOneField
from django.contrib.auth.models import User

"""Unregister Part"""
admin.site.unregister(Group)

"""Register part"""


@admin.register(Article)
class ArticleViews(admin.ModelAdmin):
    list_display = ('code_article', 'libelle',
                    'conditionnement','prix_vente',
                    'gencode', 'image', 'actif')
    list_filter = ['code_article', 'libelle']
    ordering = ('libelle',)
    search_fields = ('libelle', 'code_article', 'gencode', )
    fieldsets = (
        ('Choisir sa visibilité', {'fields': ('actif',)}),

    )


# prepopulated_fields = {'slug': ('libelle',)}

# class ArticlesInLine(admin.TabularInline):
#     model = Article
#     raw_id_fields = ['article']

@admin.register(Historique)
class HistoriqueViews(admin.ModelAdmin):
    list_display = ['date', 'get_articles', 'utilisateur']
    list_filter = ['date']
    # inlines = [ArticlesInLine]


# CustomUser
class CustomUserAdmin(UserAdmin):
    # exclude = ('username',)
    list_display = ('username', 'last_name', 'first_name', 'email', 'is_active',)
    # list_editable = ('username', 'is_active')
    fieldsets = (
        ('Informations personnelles', {'fields': (
            'email',
            'password'
        )}),

        # ('Important dates', {'fields': (
        #     'last_login',
        #     'date_joined')}),

        ('Permissions', {'fields': ('is_active',
                                    # 'is_staff',
                                    # 'is_superuser',
                                    # 'groups',
                                    # 'user_permissions'
                                    )}),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

""" Site visual """

admin.site.site_header = 'Administration Berard Distribution'
