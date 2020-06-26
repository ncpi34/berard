from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.html import format_html

from website.helpers import RandomFileName


class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    code_client = models.CharField(max_length=30)
    tarif = models.CharField(max_length=10)

    def __str__(self):
        return self.code_client


class Groupe(models.Model):
    nom = models.CharField(max_length=100,
                           unique=True)

    def __str__(self):
        return self.nom


class Famille(models.Model):
    nom = models.CharField(max_length=100)
    # groupe = models.ForeignKey(Groupe,
    #                            null=True,
    #                            on_delete=models.CASCADE,
    #                            related_name='family_by_group')
    groupe = models.ManyToManyField(Groupe,
                                    related_name='family_by_group')

    class Meta:
        ordering = ('nom',)
        verbose_name = 'family'
        verbose_name_plural = 'families'

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        print('familly')
        print(self.nom)
        return reverse('website:products_by_family',
                       args=[self.nom])


class SousFamille(models.Model):
    nom = models.CharField(max_length=100)
    # famille = models.ForeignKey(Famille,
    #                             null=True,
    #                             on_delete=models.CASCADE,
    #                             related_name='sub_family_by_family')
    famille = models.ManyToManyField(Famille,
                                     related_name='sub_family_by_family')

    class Meta:
        ordering = ('nom',)
        verbose_name = 'sub_family'
        verbose_name_plural = 'sub_families'

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        print('subfamilly')
        print(self.nom)
        return reverse('website:products_by_sub_family',
                       args=[self.nom])


class Article(models.Model):
    code_article = models.CharField(max_length=25, null=True)
    # slug = models.SlugField(max_length=200, db_index=True)
    libelle = models.CharField(max_length=150, null=True)
    conditionnement = models.CharField(null=True,
                                       max_length=30)
    prix_vente = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_1 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_2 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_3 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_4 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    gencode = models.CharField(max_length=40, null=True)
    taux_TVA = models.IntegerField(null=True)
    actif = models.BooleanField(default=True)
    groupe = models.ForeignKey(Groupe,
                               on_delete=models.CASCADE,
                               related_name='article_by_group',
                               null=True)
    famille = models.ForeignKey(Famille,
                                on_delete=models.CASCADE,
                                related_name='article_by_familly',
                                null=True)
    sous_famille = models.ForeignKey(SousFamille,
                                     on_delete=models.CASCADE,
                                     related_name='article_by_sub_familly',
                                     null=True)
    image = models.TextField(null=True, blank=True)

    # image = models.ImageField(upload_to=RandomFileName('img/'), null=True, blank=True)
    # image = models.ImageField(upload_to='img/%Y/%m/%d,  null=True, blank=True)

    class Meta:
        ordering = ['code_article']
        verbose_name = 'article'
        # index_together = (('id', 'code_article'), )

    def __str__(self):
        return '{}'.format(self.libelle)

    def get_absolute_url(self):
        return reverse('website:product_detail',
                       args=[self.id])
    # def get_img(self):
    #     if self.image:
    #         return format_html('<img src="{url}" width="50" height="50" />'.format(
    #             url=self.image
    #         ))
    #     else:
    #         return format_html('<img src="{url}" width="50" height="50" />'.format(
    #             url='/media/img/nophoto.png'
    #         ))
    #
    # get_img.short_description = 'Image'
    # get_img.allow_tags = True


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
        return reverse('website:order_detail',
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


class ProduitCommande(models.Model):
    commande = models.ForeignKey(HistoriqueCommande,
                                 related_name='items',
                                 on_delete=models.CASCADE)
    article = models.ForeignKey(Article,
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
