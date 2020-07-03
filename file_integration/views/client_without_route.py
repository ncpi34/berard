import codecs
import ftplib
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


class ClientAutomate:
    @staticmethod
    def concat(val_1, val_2):
        return val_1 + val_2

    # to convert to int without errors
    @staticmethod
    def convert_to_int(self):
        try:
            int(self)
            if int(self) > 4:
                return 0
            else:
                return int(self)
        except ValueError:
            return 0

        # Insert in DB

    @staticmethod
    def insert_into_db(self):
        print('beginning db insert')
        for rst in self:
            try:
                print(rst['email'])
                user = User.objects.update_or_create(
                    email=rst["email"],
                    username=rst["code_client"],

                    defaults=dict(
                        last_name=rst['nom'],
                        password=rst["mot_de_passe"],
                    )

                )
                # to encrypt Password
                # user.set_password(rst["mot_de_passe"])
                # user.save()
                print('RESULT', user.qs)
                ProfilUtilisateur.objects.update_or_create(
                    utilisateur=user,

                    adresse=rst["adresse"],
                    telephone=rst["telephone"],
                    tarif=rst["tarif"],
                    code_client=rst["code_client"],

                )
                print('inserted')
            except Exception:
                try:
                    print(rst['email'])
                    user = User.objects.filter(username=rst["code_client"]).update(
                        email=rst["email"],
                        username=rst["code_client"],
                        last_name=rst['nom'],
                        password=rst["mot_de_passe"],

                    )
                    ProfilUtilisateur.objects.filter(utilisateur=user).update(
                        utilisateur=user,
                        adresse=rst["adresse"],
                        telephone=rst["telephone"],
                        tarif=rst["tarif"],
                        code_client=rst["code_client"],

                    )
                except Exception as err:
                    print('not inserted', rst['code_client'])
                    print(err)
                    raise err
            # except Exception as err:
            #     print('not inserted', rst['code_client'])
            #     print(err)
            #     raise err

    # Index_method
    @classmethod
    def file_treatement(cls, **kwargs):
        host = "213.215.12.22"
        user = "admin"
        passw = "cMp5jU1C"

        try:
            # if path not exists
            path = 'resources/import/'
            if not os.path.exists(path):
                os.makedirs(path)

            # FTP
            ftp = FTP(host)
            ftp.login(user, passw)
            ftp.cwd('/Rep/EXPORT')
            ftp.retrbinary('RETR TCLT.PLN', open(os.path.join(path, 'TCLT.PLN'), 'wb').write)
            ftp.quit()

            # zz = codecs.encode('TART.PLN', encoding='utf-8', errors='strict')
            # file = open(zz, 'r')
            # text_lines = file.readlines()

            with open(os.path.join(path, 'TCLT.PLN'), encoding='utf-8', errors='ignore') as file:
                text_lines = file.readlines()

            # array of dict
            obj_bdd = [{
                "code_client": val[10:16],
                "nom": val[26:52],
                'mot_de_passe': val[10:16] + val[146:151],
                "adresse": val[26:171].strip(),
                "telephone": val[182:196],
                "tarif": cls.convert_to_int(val[232]),
                # "prenom": val[438:509],
                "email": val[438:509].strip(),

            } for val in text_lines]
            # print([val[230:240] for val in text_lines])

            cls.insert_into_db(obj_bdd)  # call method to insert in db

            resp = json.dumps(obj_bdd)
            file.close()
            return True

        except Exception as error:
            print("Error: {0}".format(error))
            return False
            # return HttpResponse(500, content_type="application/json")
