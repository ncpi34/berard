from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.html import format_html

from website.helpers import RandomFileName


class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=10)
    adresse = models.CharField(max_length=100)
    code_client = models.CharField(max_length=10)
    tarif = models.CharField(max_length=10)
    actif = models.BooleanField(default=False)

    def __str__(self):
        return self.code_client


class Groupe(models.Model):
    nom = models.CharField(max_length=40)

    def __str__(self):
        return self.nom


class Famille(models.Model):
    nom = models.CharField(max_length=40)
    groupe = models.ForeignKey(Groupe,
                               on_delete=models.CASCADE,
                               related_name='familly_by_group')

    class Meta:
        ordering = ('nom',)
        verbose_name = 'familly'
        verbose_name_plural = 'famillies'

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('website:products_by_familly',
                       args=[self.nom])


class Article(models.Model):
    code_article = models.CharField(max_length=15)
    # slug = models.SlugField(max_length=200, db_index=True)
    libelle = models.CharField(max_length=40)
    conditionnement = models.CharField(max_length=30)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    gencode = models.IntegerField()
    taux_TVA = models.IntegerField()
    actif = models.BooleanField(default=False)
    groupe = models.ForeignKey(Groupe,
                               on_delete=models.CASCADE,
                               related_name='article_by_group')
    famille = models.ForeignKey(Famille,
                                on_delete=models.CASCADE,
                                related_name='article_by_familly')
    image = models.TextField()
    # image = models.ImageField(upload_to=RandomFileName('img/'), null=True, blank=True)
    # image = models.ImageField(upload_to='img/%Y/%m/%d,  null=True, blank=True)

    class Meta:
        ordering = ['code_article']
        verbose_name = 'article'
        # index_together = (('id', 'code_article'), )

    def __str__(self):
        return self.libelle

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


class Historique(models.Model):
    date = models.DateTimeField(auto_now=True)
    article = models.ManyToManyField(Article)

    # utilisateur = models.ManyToOneRel(User)

    def __str__(self):
        return self.date
