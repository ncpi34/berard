import django_filters
from django.forms import TextInput

from website.models import Article


class ArticleFilter(django_filters.FilterSet):
    code_article = django_filters.CharFilter(label='',
                                             lookup_expr='icontains',
                                             widget=TextInput(attrs={

                                                 'class': 'searchTerm',
                                                 'placeholder': 'code article',
                                                 'style':
                                                     'border-radius: 4px;color:white;'
                                                     'text:center;'
                                                     'background-color:white;'
                                             })
                                             )

    class Meta:
        model = Article
        fields = ['code_article']
