import django_filters

from website.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'code_article': ['icontains'],
            # 'libelle':  ['icontains'],
            # 'famille__nom': ['icontains']
        }

