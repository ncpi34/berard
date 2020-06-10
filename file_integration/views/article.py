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

    # GROUP
    @staticmethod
    def check_group(self):
        if self:
            find = re.search(',', self)
            if find:
                table_split = self.replace(',', ' ').replace('-', ' ').split()
                if table_split:
                    if len(table_split) > 4:
                        return int(table_split[-3].lstrip('0'))
                    else:
                        return int(table_split[1].lstrip('0'))
                else:
                    return int(self[0:2].lstrip('0'))
        else:
            # print('ERROR: no group')
            return ""

    # FAMILY
    @staticmethod
    def check_family(self):
        if self:
            if re.search(',', self):
                table_split = self.replace(',', ' ').replace('-', ' ').split()
                if table_split:
                    if len(table_split) > 4:
                        return int(table_split[-2].lstrip('0'))
                    else:
                        return int(table_split[1].lstrip('0'))
                else:
                    return int(self[0:2].lstrip('0'))
        else:
            # print('ERROR: no familly')
            return ""

    # NAME_PRODUCT
    @staticmethod
    def check_name(name, val_to_check):
        if name and val_to_check:
            table_split = val_to_check.replace(',', ' ').replace('-', ' ').split()
            if table_split:
                if len(table_split) > 4:
                    # print(table_split)
                    # print(name + ' ' + concatenation)
                    concatenation = ' '.join(table_split[0:-4])
                    return name + ' ' + concatenation
                else:
                    return name
            else:
                return ''
        else:
            # print('ERROR: no name product')
            return ""

    # Conditionning
    @staticmethod
    def check_conditionning(val_to_check, second_val):
        if second_val and val_to_check:
            # print((val_to_check, second_val))
            if re.search(',', val_to_check):
                try:
                    match = re.search(r'[+-]?\d+,', val_to_check)
                    if match:
                        match_split = match.group().replace(',', '')
                        if len(match_split) > 2 and int(match_split[-2:]) <= 50:
                            return int(match_split[-2:])
                        elif len(match_split) > 2 and int(match_split[-2:]) > 50:
                            print()
                            return int(match_split[-1:])
                        else:
                            return int(match_split)
                except ValueError:
                    return 0

            elif re.search(',', second_val):
                try:
                    match = re.search(r'[+-]?\d+,', second_val)
                    if match:
                        match_split = match.group().replace(',', '')
                        if len(match_split) > 2 and int(match_split[-2:]) <= 50:
                            return int(match_split[-2:])
                        elif len(match_split) > 2 and int(match_split[-2:]) > 50:
                            return int(match_split[-1:])
                        else:
                            return int(match_split)
                except ValueError:
                    return 0

            else:
                # print('ERROR: no data in file for conditionning')
                return 0
        else:
            # print('ERROR: no conditionning name')
            return 0

    # check if string could be convert to float
    @staticmethod
    def is_float(val_to_test, second_val, third_val):
        if val_to_test and second_val and third_val:
            try:
                res = float(val_to_test.replace(',', '.'))
                return res

            except ValueError:
                try:
                    res = float(second_val.replace(',', '.'))
                    return res
                except ValueError:
                    res = float(third_val.replace(',', '.'))
                    return res

        else:
            return float(0.00)

    # check if string could be convert to float with two decimals
    @staticmethod
    def is_float_with_two_decimals(val_to_test, second_val):
        if val_to_test and second_val:
            try:
                res = float(val_to_test.replace(',', '.'))
                return res

            except ValueError:
                res = round(float(second_val.replace(',', '.')), 2)
                return res

        else:
            return float(0.00)

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
            reg = [(re.split(r"\s{2,}", item)) for item in text_lines]  # multidimensional list

            # array of dict
            obj_bdd = [{
                "code_article": val[0][10:16],
                "libelle": cls.check_name(val[1], val[2]),
                "prix_vente": cls.is_float_with_two_decimals(val[-6], val[-7]),
                "prix_achat_1": cls.is_float(val[4], val[5], val[6]),
                "prix_achat_2": cls.is_float(val[5], val[6], val[7]),
                "prix_achat_3": cls.is_float(val[6], val[7], val[8]),
                "prix_achat_4": cls.is_float(val[7], val[8], val[9]),
                "gencode": val[-8][0:-1],
                # "conditionnement": cls.check_conditionning(val[-17], val[-16]),
                "conditionnement": cls.check_conditionning(val[1], val[2]),
                # "taux_TVA": 6,  # TO DEFINE
                "groupe": cls.check_group(val[2]),
                "famille": cls.check_family(val[2]),
            } for val in reg]

            # print([i['libelle'] for i in obj_bdd])
            # print(obj_bdd[2])
            # print(obj_bdd[16])
            # print(obj_bdd[4249])

            cls.insert_into_db(obj_bdd)  # call method to insert in db
            # resp = json.dumps(obj_bdd[1557])
            resp = json.dumps(obj_bdd)
            return HttpResponse(resp, content_type='application/json')
            # return render(request, obj_bdd)

        except OSError as error:
            print("OS error: {0}".format(error))
            raise error
