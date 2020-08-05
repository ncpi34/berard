from django.db import models
from django.contrib.postgres.fields import JSONField


class PanierEnCours(models.Model):
    utilisateur = models.IntegerField()
    donnees = JSONField()

    def __unicode__(self):
        return self.utilisateur
