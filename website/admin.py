from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.text import Truncator

from website.models import ProfilUtilisateur, Article, Favori
from order.models import HistoriqueCommande, ProduitCommande
from django.db.models import ManyToOneRel, ForeignKey, OneToOneField
from django.contrib.auth.models import User

"""Unregister Part"""
admin.site.unregister(Group)

"""Register part"""

""" Article """


@admin.register(Article)
class ArticleViews(admin.ModelAdmin):
    list_display = ('code_article', 'libelle',
                    'conditionnement', 'prix_vente',
                    'gencode', 'image', 'actif')
    list_filter = ['code_article', 'libelle']
    ordering = ('libelle',)
    search_fields = ('libelle', 'code_article', 'gencode',)
    fieldsets = (
        ('Choisir sa visibilité',
         # 'description': 'une description',
         # 'classes': 'wide' or 'extrapretty' or 'collapse',
         {'fields': ('actif',)}),

    )


# prepopulated_fields = {'slug': ('libelle',)}

class ArticlesInLine(admin.TabularInline):
    model = ProduitCommande
    raw_id_fields = ['article']


""" Order Summary """


@admin.register(HistoriqueCommande)
class HistoriqueViews(admin.ModelAdmin):
    list_display = ['date', 'get_articles', 'utilisateur']
    list_filter = ['date']
    date_hierarchy = 'date'
    inlines = [ArticlesInLine]

    # def show_content_part(self, article):
    #     """
    #     Retourne les 40 premiers caractères du contenu de l'article,
    #     suivi de points de suspension si le texte est plus long.
    #     """
    #     return Truncator(article.contenu).chars(40, truncate='...')
    #
    # # En-tête de notre colonne
    # show_content_part.short_description = 'Aperçu du contenu'


# admin.site.register(Historique, HistoriqueViews)


""" CustomUser """


class CustomUserAdmin(UserAdmin):
    # exclude = ('username',)
    list_display = ('username', 'last_name', 'first_name', 'email', 'is_active',)
    # list_editable = ('username', 'is_active')
    fieldsets = (
        ('Informations personnelles', {'fields': (
            'email',
            'password',
            # 'profilutilisateur__tarif'
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

    def get_queryset(self, request):  # exclude user with tarif equal to 0
        qs = super().get_queryset(request)
        return qs.exclude(profilutilisateur__tarif=0)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

""" Favorite"""
# @admin.register(Favoris)
# class ArticleViews(admin.ModelAdmin):
#     list_display = ('code_article', 'libelle',
#                     'conditionnement', 'prix_vente',
#                     'gencode', 'image', 'actif')
#     list_filter = ['code_article', 'libelle']
#     ordering = ('libelle',)
#     search_fields = ('libelle', 'code_article', 'gencode',)
#     fieldsets = (
#         ('Choisir sa visibilité',
#          # 'description': 'une description',
#          # 'classes': 'wide' or 'extrapretty' or 'collapse',
#          {'fields': ('actif',)}),
#
#     )
admin.site.register(Favori)
"""Unregister part"""
admin.site.unregister(HistoriqueCommande)

""" Site visual """
admin.site.site_header = 'Administration Berard Distribution'
