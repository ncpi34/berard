from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class PanierEnCours(models.Model):
    utilisateur = models.IntegerField()
    donnees = JSONField()

    def __unicode__(self):
        return self.utilisateur
