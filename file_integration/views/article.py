import re
from ftplib import FTP
import os
import string
import numpy as np

import json
from django.http import HttpResponse
from django.shortcuts import render
from website.models import Article

""" Article File"""


class ArticleViews(object):
    # change to float
    @staticmethod
    def is_integer(self):
        try:
            integer =int(self)
            return integer
        except ValueError:
            try:
                str_split = self.split(',')
                return int(str_split[0])
            except ValueError:
                return self

    # change to integer
    @staticmethod
    def is_float(self):
        try:
            float_self = float(self.replace(',', '.'))
            return float_self
        except ValueError:
            return 0.00

    # Insert in DB
    @staticmethod
    def insert_into_db(self):
        for rst in self:
            try:
                print('beginning db insert')
                print(rst['libelle'])
                article, created = Article.objects.update_or_create(
                    libelle=rst['libelle'],
                    # libelle=rst['libelle'].lower(),
                    code_article=rst["code_article"],
                    prix_vente=rst["prix_vente"],
                    prix_achat_1=rst["prix_achat_1"],
                    prix_achat_2=rst["prix_achat_2"],
                    prix_achat_3=rst["prix_achat_3"],
                    prix_achat_4=rst["prix_achat_4"],
                    gencode=rst["gencode"],
                    conditionnement=rst["conditionnement"],
                    # taux_TVA=rst["taux_TVA"],
                    # groupe=rst["groupe"],
                    # famille=rst["famille"],
                )

                # article.save
                # article.groupe.add(rst["groupe"])
                # article.famille.add(rst["famille"])
                print('inserted')
            except Exception as err:
                print(err)
                raise err

    # Index_method
    @classmethod
    def file_treatement(cls, request, **kwargs):
        host = "213.215.12.22"
        user = "admin"
        passw = "cMp5jU1C"

        try:
            # LOCAL
            # a = open('TEST.PLN', 'r')

            # FTP
            ftp = FTP(host, user, passw)
            ftp.cwd('/Rep/EXPORT')
            a = open('TART.PLN', 'r')

            text_lines = a.readlines()

            # array of dict
            obj_bdd = [{
                "code_article": cls.is_integer(val[10:16]),
                "libelle": val[18:54],
                "conditionnement": cls.is_integer(val[54:58]),

                "prix_achat_1": cls.is_float(val[83:91]),
                "prix_achat_2": cls.is_float(val[91:99]),
                "prix_achat_3": cls.is_float(val[99:107]),
                "prix_achat_4": cls.is_float(val[107:115]),
                "prix_vente": cls.is_float(val[161:169]),

                "gencode": val[228:241],
                # # "taux_TVA": 6,  # TO DEFINE

                "groupe": cls.is_integer(val[58:60]),
                "famille": cls.is_integer(val[62:64]),
                "sous_famille": cls.is_integer(val[66:68]),
            } for val in text_lines]

            # print([i['code_article'] for i in obj_bdd])

            cls.insert_into_db(obj_bdd)  # call method to insert in db

            resp = json.dumps(obj_bdd)
            return HttpResponse(resp, content_type='application/json')


        except OSError as error:
            print("OS error: {0}".format(error))
            raise error
