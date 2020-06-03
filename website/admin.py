from django.contrib import admin
from django.contrib.auth.models import Group
from website.models import ProfilUtilisateur, Article, Historique
from django.db.models import ManyToOneRel, ForeignKey, OneToOneField
from django.contrib.auth.models import User

"""Admin Part"""
# Unregister parts
admin.site.unregister(Group)


# Register parts

@admin.register(ProfilUtilisateur)
class UsersViews(admin.ModelAdmin):
    list_display = ['utilisateur', 'telephone', 'adresse',
                    'code_client', 'tarif', 'actif']
    list_filter = ['code_client', 'actif']
    list_editable = ['actif', 'code_client']

# admin.site.unregister(User)
# admin.site.register(UsersViews)

admin.site.register(Article)
# @admin.register(Article)
# class ArticleViews(admin.ModelAdmin):
#     list_display = ['code_article', 'libelle', 'conditionnement',
#                     'prix_vente', 'prix_achat', 'gencode', 'taux_TVA', 'actif',
#                     'groupe', 'famille', 'image']
#     list_filter = ['code_article', 'libelle']
#     list_editable = ['actif']
    # prepopulated_fields = {'slug': ('libelle',)}
    
# class ArticlesInLine(admin.TabularInline):
#     model = Article
#     raw_id_fields = ['article']


@admin.register(Historique)
class HistoriqueViews(admin.ModelAdmin):
    list_display = ['date', 'get_articles', 'utilisateur']
    list_filter = ['date']
    # inlines = [ArticlesInLine]
