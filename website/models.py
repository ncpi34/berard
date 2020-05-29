from django.contrib.auth.models import User
from django.db import models


# Create your models here.
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

    def __str__(self):
        return self.nom


class Article(models.Model):
    code_article = models.CharField(max_length=15)
    libelle = models.CharField(max_length=40)
    conditionnement = models.CharField(max_length=30)
    prix_vente = models.FloatField()
    prix_achat = models.FloatField()
    gencode = models.IntegerField()
    taux_TVA = models.IntegerField()
    actif = models.BooleanField(default=False)
    groupe = models.ForeignKey(Groupe,
                               on_delete=models.CASCADE,
                               related_name='article_by_group')
    famille = models.ForeignKey(Famille,
                                on_delete=models.CASCADE,
                                related_name='article_by_familly')
    image = models.CharField(max_length=4000)
    # image = models.ImageField(upload_to=RandomFileName('img/'), null=True, blank=True)

    # def __str__(self):
    #     return "%s %s" % (self.libelle, self.code_article)
    #
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

    class Meta:
        ordering = ['code_article']


class Historique(models.Model):
    date = models.DateTimeField(auto_now=True)
    article = models.ManyToManyField(Article)
    # utilisateur = models.ManyToOneRel(User)

    def __str__(self):
        return self.date
