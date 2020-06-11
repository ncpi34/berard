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


class ClientAlgoViews(object):

    # ADDRESS -> check if last part is a phone number or not
    @staticmethod
    def check_adress(val_to_check):
        if val_to_check:
            try:
                int(val_to_check[-2:])
                return ""
            except ValueError:
                return val_to_check
        else:
            # print('ERROR: no address name')
            return ""

    # Phone number -> check if last part is a phone number or not
    # and use only a part because sometimesthere is two numbers
    @staticmethod
    def check_phone_number(first_val_to_check, second_val_to_check):
        if first_val_to_check and second_val_to_check:
            try:
                supp_points = first_val_to_check.replace('.', '')
                int(supp_points[-12:])
                if len(supp_points) > 14:
                    return supp_points[15:29]
                return supp_points

            except ValueError:
                try:
                    int(first_val_to_check[-2:])
                    if len(first_val_to_check) > 14:
                        return first_val_to_check[15:29].replace('.', '')
                    return first_val_to_check.replace('.', '')

                except ValueError:
                    try:
                        supp_points = first_val_to_check.replace('.', '')
                        int(supp_points[-12:])
                        if len(supp_points) > 14:
                            return supp_points[15:29]
                        return supp_points

                    except ValueError:
                        try:
                            int(second_val_to_check[-2:])
                            if len(second_val_to_check) > 14:
                                return second_val_to_check[15:29].replace('.', '')
                            return second_val_to_check.replace('.', '')
                        except ValueError:
                            return '0000000000'
            # except ValueError:
            #     return '00 00 00 00 00'
        else:
            # print('ERROR: no phone number')
            return '0000000000'

    # check if email and split it to get clean email
    @staticmethod
    def check_email(first_val_to_check, second_val_to_check):
        if first_val_to_check and second_val_to_check:
            try:
                match = re.search(r'@', first_val_to_check)
                if match:
                    last_index = 0
                    for i in range(0, len(first_val_to_check)):
                        try:
                            int(first_val_to_check[i])
                            last_index = i
                        except ValueError:
                            break

                    return first_val_to_check[last_index + 4:]
                else:
                    return ''

            except ValueError:
                try:
                    match = re.search(r'@', second_val_to_check)
                    if match:
                        last_index = 0
                        for i in range(0, len(second_val_to_check)):
                            # print(second_val_to_check[i])
                            try:
                                int(second_val_to_check[i])
                                last_index = i
                            except ValueError:
                                break

                        return second_val_to_check[last_index + 4:]
                    else:
                        return ''

                except ValueError:
                    return ''
        else:
            return ''

    # Check tarif
    @staticmethod
    def check_tarif(first_val_to_check, second_val_to_check):
        if first_val_to_check and second_val_to_check:
            len_1 = len(first_val_to_check)
            len_2 = len(second_val_to_check)
            if len_1 == 1:
                return int(first_val_to_check)
            elif len_2 == 1:
                return int(second_val_to_check)
            else:
                return 0
        else:
            return ''

    # Check client_code
    @staticmethod
    def check_client_code(first_val_to_check, second_val_to_check):
        if first_val_to_check and second_val_to_check:
            if len(first_val_to_check) > 6:
                return first_val_to_check[-8:]
            elif len(second_val_to_check) > 6:
                return second_val_to_check[-8:]
            else:
                return ''
        else:
            return''


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
                    password=rst["email"],
                    username=rst["code_client"]

                    # adresse=rst["adresse"],
                    # telephone=rst["telephone"],
                    # tarif=rst["tarif"],
                    # numero_client=rst["numero_client"],
                )
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
            a = open('TCLT_TEST.PLN', 'r')

            # FTP
            # ftp = FTP(host, user, passw)
            # ftp.cwd('/Rep/EXPORT')
            # # print(ftp.dir())
            # a = open('TCLT.PLN', 'r')

            text_lines = a.readlines()
            reg = [(re.split(r"\s{2,}", item)) for item in text_lines]  # multidimensional list
            # print(reg)

            # array of dict
            obj_bdd = [{
                "nom": val[1],
                # "prenom": val[1],
                "adresse": val[1] + ' ' + val[2] + ' ' + val[3] + ' ' + cls.check_adress(val[4]),
                "telephone": cls.check_phone_number(val[4], val[5]),
                "email": cls.check_email(val[-2], val[-1]),
                "tarif": cls.check_tarif(val[5], val[6]),
                "code_client": cls.check_client_code(val[0], val[1]),

            } for val in text_lines]




            # print(obj_bdd[2])
            # print(obj_bdd[16])
            # print(obj_bdd[4249])

            # cls.insert_into_db(obj_bdd)  # call method to insert in db
            # resp = json.dumps(obj_bdd[1557])
            resp = json.dumps(obj_bdd)
            return HttpResponse(resp, content_type='application/json')
            # return render(request, 'home.html')

        except OSError as error:
            print("OS error: {0}".format(error))
            raise error
