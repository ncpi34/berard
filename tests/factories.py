import factory


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'website.Article'  # Equivalent to ``model = myapp.models.User``
        # django_get_or_create = ('code_article','libelle', 'conditionnement',
        #                         'prix_vente', 'prix_achat', 'gencode',
        #                         'taux_TVA', 'groupe', 'famille')

    libelle = 'john'
