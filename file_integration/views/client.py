import re
from ftplib import FTP
import os
import string
import numpy as np

import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from website.models import Article, ProfilUtilisateur

""" Client File"""


class ClientViews(object):

    # Insert in DB
    @staticmethod
    def insert_into_db(self):
        for rst in self:
            try:
                print('beginning db insert')
                print(rst['email'])
                user, created = User.objects.update_or_create(
                    # last_name=rst['nom'],
                    # first_name=rst["prenom"],
                    email=rst["email"],
                    # password=rst["email"],
                    username=rst["code_client"]

                )
                user.set_password(rst["email"])
                user.save()
                user_one_to_one = ProfilUtilisateur.objects.update_or_create(
                    utilisateur=user,
                    adresse=rst["adresse"],
                    telephone=rst["telephone"],
                    tarif=rst["tarif"],
                    code_client=rst["code_client"],
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
            # a = open('TCLT_TEST.PLN', 'r')

            # FTP
            ftp = FTP(host, user, passw)
            ftp.cwd('/Rep/EXPORT')
            # print(ftp.dir())
            a = open('TCLT.PLN', 'r')

            text_lines = a.readlines()

            # array of dict

            obj_bdd = [{
                # "nom": val[1],
                # # "prenom": val[1],
                "email": val[438:509],
                "tarif": int(val[232]),
                "telephone": val[182:196],
                "adresse": val[26:171].replace('  ', ' '),
                "code_client": val[10:17],

            } for val in text_lines]

            cls.insert_into_db(obj_bdd)  # call method to insert in db

            resp = json.dumps(obj_bdd)
            return HttpResponse(resp, content_type='application/json')

        except OSError as error:
            print("OS error: {0}".format(error))
            raise error
