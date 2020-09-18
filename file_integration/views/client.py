import codecs
import ftplib
import re
from ftplib import FTP
import os
import string
import numpy as np

import json

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from website.models import Article, ProfilUtilisateur
from django.core.exceptions import ObjectDoesNotExist

""" Client File"""


class ClientViews(object):
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
        for iteration, rst in enumerate(self):
            try:
                user, created = User.objects.update_or_create(
                    username=rst["code_client"],

                    defaults=dict(
                        email=rst["email"],
                        last_name=rst['nom'],
                        password=rst["mot_de_passe"], )
                )

                """ if suppress client """
                # # check if user has tarif equal to 0
                # if rst['tarif'] == 0:
                #     try:
                #         user = User.objects.get(username=rst["code_client"])
                #         user.delete()
                #         print('user delete', rst["code_client"])
                #     except ObjectDoesNotExist:
                #             pass
                # else:
                #     user.is_active = True
                #     user.save()
             
                #     try:
                #         user.profilutilisateur.code_representant = rst["code_representant"]
                #         user.profilutilisateur.adresse = rst["adresse"]
                #         user.profilutilisateur.telephone = rst["telephone"]
                #         user.profilutilisateur.tarif = rst["tarif"]
                #         user.profilutilisateur.code_client = rst["code_client"]
                #         user.profilutilisateur.save()
                #         print('profile done')
                #     except ObjectDoesNotExist as err:
                #         print('!!!!!!!!!!!profile error!!!!!!!!!!!!!')
                #         raise err
                """ endif """

                # check if user has tarif equal to 0
                if rst['tarif'] == 0:
                    user.is_active = False
                    user.save()
                else:
                    user.is_active = True
                    user.save()
              
                try:
                    user.profilutilisateur.code_representant = rst["code_representant"]
                    user.profilutilisateur.adresse = rst["adresse"]
                    user.profilutilisateur.telephone = rst["telephone"]
                    user.profilutilisateur.tarif = rst["tarif"]
                    user.profilutilisateur.code_client = rst["code_client"]
                    user.profilutilisateur.save()
                   
                except ObjectDoesNotExist as err:
                    raise err

               

            except Exception as err:
                raise err

    # Index_method
    @classmethod
    def file_treatement(cls, request, **kwargs):
        if kwargs['password'] == 'berard_client':
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
                    "code_representant": val[4:7].strip(),
                    "code_client": val[10:16],
                    "nom": val[26:52],
                    'mot_de_passe': val[10:16] + val[146:151],
                    "adresse": val[26:171].strip(),
                    "telephone": val[182:196],
                    "tarif": cls.convert_to_int(val[232]),
                    # "prenom": val[438:509],
                    "email": val[438:509].strip(),

                } for val in text_lines]
                
                cls.insert_into_db(obj_bdd)  # call method to insert in db

                file.close()
                return HttpResponse(200, content_type='application/json')
                
            except Exception as error:
                raise error
                
        else:
            return HttpResponseBadRequest("Vous n'avez pas les accés")
            
