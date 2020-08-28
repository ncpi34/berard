from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from pathlib import Path
from website.helpers import RandomFileName
from django.db.models import Q
from django.db.models import Count
from django.core.exceptions import ValidationError
from website.models import Article
from django.utils import timezone

""" Order Summary """


class HistoriqueCommande(models.Model):
    date = models.DateTimeField(auto_now=True)
    utilisateur = models.ForeignKey(User,
                                    related_name='user',
                                    on_delete=models.CASCADE,
                                    null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return 'Commande {}'.format(self.id)

    def get_absolute_url(self):
        return reverse('order:order_detail',
                       args=[self.id])

    def get_number_products(self):
        total = 0
        for item in self.items.all():
            total += item.quantite
        return total

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # def get_total_cost_by_article(self):
    #     return sum(item.get_cost() for item in self.items.all())

    def get_articles(self):
        return [item.get_article() for item in self.items.all()]


""" Order """


class ProduitCommande(models.Model):
    commande = models.ForeignKey(HistoriqueCommande,
                                 null=True,
                                 related_name='items',
                                 on_delete=models.CASCADE)
    article = models.ForeignKey(Article,
                                null=True,
                                related_name='orders_items',
                                on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=100,
                               decimal_places=2,
                               default=0)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.prix * self.quantite

    def get_article(self):
        return self

