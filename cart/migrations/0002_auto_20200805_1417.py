# Generated by Django 3.0.5 on 2020-08-05 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='panierencours',
            old_name='donnes',
            new_name='donnees',
        ),
    ]
