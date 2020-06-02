import django_filters

from website.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'libelle':  ['icontains'],
            # 'famille__nom': ['icontains']
        }

