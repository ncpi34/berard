from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from pathlib import Path
from website.helpers import RandomFileName
from django.db.models import Q
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

""" Profil """


class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    code_client = models.CharField(max_length=30)
    tarif = models.CharField(max_length=10)
    code_representant = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.code_client

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        # instance.profile.save()
        if created:
            ProfilUtilisateur.objects.get_or_create(utilisateur=instance)
        ProfilUtilisateur.objects.get_or_create(utilisateur=instance)    
        # instance.profilutilisateur.save()    


""" Group """


class Groupe(models.Model):
    nom = models.CharField(max_length=100,
                           unique=True)
                       

    def __str__(self):
        return self.nom


""" Family """


class Famille(models.Model):
    nom = models.CharField(max_length=100)
    groupe = models.ManyToManyField(Groupe,
                                    related_name='family_by_group')

    class Meta:
        ordering = ('nom',)
        verbose_name = 'family'
        verbose_name_plural = 'families'

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('website:products_by_family',
                       args=[self.nom])


""" SubFamily """


class SousFamille(models.Model):
    nom = models.CharField(max_length=100)
    famille = models.ManyToManyField(Famille,
                                     related_name='sub_family_by_family')

    class Meta:
        ordering = ('nom',)
        verbose_name = 'sub_family'
        verbose_name_plural = 'sub_families'

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('website:products_by_sub_family',
                       args=[self.nom])


""" Article """


class Article(models.Model):
    code_article = models.CharField(max_length=25, null=True)
    # slug = models.SlugField(max_length=200, db_index=True)
    libelle = models.CharField(max_length=150, null=True)
    nb_vues = models.IntegerField(default=0)
    conditionnement = models.CharField(null=True,
                                       max_length=30)
    prix_vente = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_1 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_2 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_3 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    prix_achat_4 = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    gencode = models.CharField(max_length=40, null=True)
    taux_TVA = models.FloatField(null=True)
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

    class Meta:
        ordering = ['code_article']
        verbose_name = 'article'
        # index_together = (('id', 'code_article'), )

    def __str__(self):
        return '{}'.format(self.libelle)

    def get_absolute_url(self):
        return reverse('website:product_detail',
                       args=[self.id])

    def get_img(self):
        if Path("media/img/product/" + self.code_article + ".png").is_file():
            return Path("/media/img/product/" + self.code_article + ".png")
        elif Path("media/img/product/" + self.code_article + ".PNG").is_file():
            return Path("/media/img/product/" + self.code_article + ".PNG")
        elif Path("media/img/product/" + self.code_article + ".JPG").is_file():
            return Path("/media/img/product/" + self.code_article + ".JPG")
        elif Path("media/img/product/" + self.code_article + ".jpg").is_file():
            return Path("/media/img/product/" + self.code_article + ".jpg")
        elif Path("media/img/product/" + self.code_article + ".jpeg").is_file():
            return Path("/media/img/product/" + self.code_article + ".jpeg")
        else:
            return '/media/img/nophoto.jpg'
    # get_img.short_description = 'Image'
    # get_img.allow_tags = True
    def calculate_price_with_taxes(self, arg):
        return round( float(arg) * (self.taux_TVA / 100 + 1 ), 2 )
        
    def get_price_with_taxes_1(self):
        return self.calculate_price_with_taxes(self.prix_achat_1)

    def get_price_with_taxes_2(self):
        return self.calculate_price_with_taxes(self.prix_achat_2)

    def get_price_with_taxes_3(self):
        return self.calculate_price_with_taxes(self.prix_achat_3)

    def get_price_with_taxes_4(self):
        return self.calculate_price_with_taxes(self.prix_achat_4)  

    def format_VAT(self):
        if self.taux_TVA % 2 == 0.0:
            return int(self.taux_TVA)
        else:
            return self.taux_TVA     
                        

""" Offers """


class Favori(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, primary_key=True, )
    class Meta:
        verbose_name = "Favoris"
        verbose_name_plural = "Favoris"

     
    def __str__(self):
        return self.article.libelle

    def clean(self):
        numFavorites = Favori.objects.all().count()
        if numFavorites > 5:
            raise ValidationError("Vous ne pouvez pas cr??er plus de  {} favoris".format(numFavorites))


""" Favorites """


class FavorisClient(models.Model):
    utilisateur = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='user_favorite',
                                    )
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='article_favorite',
                                )
    quantite = models.IntegerField(default=0)

    def __unicode__(self):
        return self.utilisateur.id

    def __str__(self):
        return self.article.libelle

    def format_data(self):
        return {'libelle': self.article.libelle, 'quantite': self.quantite}
