import django_filters
from django.forms import TextInput

from website.models import Article


class ArticleFilter(django_filters.FilterSet):
    code_article = django_filters.CharFilter(label='',
                                             lookup_expr='icontains',
                                             widget=TextInput(attrs={
                                                 'id': 'search',
                                                 'class': 'searchTerm',
                                                 'placeholder': 'Rechercher',
                                                 'style':
                                                     'border-radius: 4px;color:white;'
                                                     'text-align:center;'
                                                     'background-color:white;'
                                                     'color:black;'
                                                     'top:1px'
                                             })
                                             )

    class Meta:
        model = Article
        fields = ['code_article']
