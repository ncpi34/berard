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
    @staticmethod
    def concat(val_1, val_2):
        print(val_2)
        return val_1 + val_2

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
                    # password=rst["mot_de_passe"],
                    username=rst["code_client"]

                )
                user.set_password(rst["mot_de_passe"])
                user.save()
                user_one_to_one = ProfilUtilisateur.objects.update_or_create(
                    utilisateur=user,
                    adresse=rst["adresse"],
                    telephone=rst["telephone"],
                    tarif=rst["tarif"],
                    code_client=rst["code_client"],
                )
                print('inserted')
            except Exception as err:
                print('not inserted', rst['code_client'])
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
            # a = open('tests/file_from_client/TCLT.PLN', 'r')
            # FTP
            ftp = FTP(host, user, passw)
            ftp.cwd('/Rep/EXPORT')
            # files = ftp.dir()
            # print(files)
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
                "code_client": val[10:16],
                'mot_de_passe':val[10:16] + val[146:151]

            } for val in text_lines]
            # print([i['mot_de_passe'] for i in obj_bdd])

            # cls.insert_into_db(obj_bdd)  # call method to insert in db

            resp = json.dumps(obj_bdd)
            return HttpResponse(resp, content_type='application/json')

        except OSError as error:
            print("OS error: {0}".format(error))
            raise error
