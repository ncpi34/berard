import re
from ftplib import FTP
import os
import string
import numpy as np
import pandas as pd
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from website.models import Article, Groupe, Famille, SousFamille
import os.path
from pyexcel_xlsx import get_data
from django.core.exceptions import ObjectDoesNotExist
from os import path
import xlsxwriter


class ArticleViews(object):
    """
    Article File
    """

    @classmethod
    def file_treatement(cls, request, **kwargs):
        if kwargs['password'] == 'berard_article':
            # if path not exists
            path = 'resources/import/'
            if not os.path.exists(path):
                os.makedirs(path)
            ftp = cls.connect_ftp(path)
            if ftp:
                try:

                    with open(os.path.join(path, 'TART.PLN'), encoding="utf-8", errors='ignore') as file:
                        text_lines = file.readlines()

                    array_of_obj = cls.build_array(text_lines)
                    cls.insert_into_db(array_of_obj)  # call method to insert in db

                    file.close()
                    cls.get_VAT()  # insert VAT from an other file

                    # cls.check_picture() # to check pictures

                    return HttpResponse(200, content_type='application/json')

                except OSError as error:
                    print("OS error: {0}".format(error))
                    return False
        else:
            return HttpResponseBadRequest("Vous n'avez pas les accés")

    @classmethod
    def build_array(cls, array):
        obj_bdd = [{
            "code_article": val[10:16].strip(),
            "libelle": val[18:54],
            "conditionnement": cls.is_integer(val[54:58]),

            "prix_achat_1": cls.is_float(val[83:91]),
            "prix_achat_2": cls.is_float(val[91:99]),
            "prix_achat_3": cls.is_float(val[99:107]),
            "prix_achat_4": cls.is_float(val[107:115]),
            "prix_vente": cls.is_float(val[161:169]),

            "gencode": val[228:241],

            "tri": val[58:68],
            "groupe": cls.is_integer(val[58:60]),
            "famille": cls.is_integer(val[61:64]),
            "sous_famille": cls.is_integer(val[65:68]),
        } for val in array]

        f = open('tri.txt', 'w')
        [f.write(i['tri'] + '\n') for i in obj_bdd]
        f.close()

        return obj_bdd

    @staticmethod
    def connect_ftp(path):
        try:
            host = '213.215.12.22'
            # host = "Berard.cloud.lcsgroup.fr"
            user = "admin"
            passw = "cMp5jU1C"
            # FTP
            ftp = FTP(host)
            ftp.login(user, passw)
            ftp.cwd('/Rep/EXPORT')
            ftp.retrbinary('RETR TART.PLN', open(os.path.join(path, 'TART.PLN'), 'wb').write)
            ftp.quit()

            return True
        except Exception as e:
            print('error ftp', e)
            raise e

    @staticmethod
    def check_picture():
        articles = Article.objects.all()
        workbook = xlsxwriter.Workbook('photo.xlsx')
        worksheet = workbook.add_worksheet()

        # Some data we want to write to the worksheet.
        expenses = (
            ['Rent', 1000],
            ['Gas', 100],
            ['Food', 300],
            ['Gym', 50],
        )

        # Start from the first cell. Rows and columns are zero indexed.
        row = 1
        col = 0

        # headers
        worksheet.write(0, 0, 'Libelle')
        worksheet.write(0, 1, 'code')
        worksheet.write(0, 2, 'gencod')
        worksheet.write(0, 3, 'rayon')
        worksheet.write(0, 4, 'famille')

        # Iterate over the data and write it out row by row.
        for item in articles:
            if not os.path.exists(f"D:\Projets\Berard\media\img\product\{item.code_article}.jpg"):
                print('item', item)
                worksheet.write(row, col, item.libelle)
                worksheet.write(row, col + 1, item.code_article)
                worksheet.write(row, col + 2, item.gencode)
                if item.groupe is not None:
                    worksheet.write(row, col + 3, item.groupe.nom)
                if item.famille is not None:
                    worksheet.write(row, col + 4, item.famille.nom)
                # worksheet.write(row, col + 1, cost)
                row += 1

        # Write a total using a formula.
        worksheet.write(row, 0, 'Total')
        print('row', row)
        worksheet.write(row, 1, f'{row - 1}')

        workbook.close()

        # for article in articles:
        #     print(article)
        # os.path.exists("file.txt")
        return 'rr'

    @staticmethod
    def get_errors_on_three_values(val_1, val_2, val_3):
        try:
            int(val_1)
            print(int(val_1))
        except ValueError:
            try:
                int(val_2)
                print(int(val_2))
            except ValueError:
                try:
                    int(val_3)
                    print(int(val_3))
                except ValueError:
                    print('error on three values')

    # Check errors
    @staticmethod
    def get_error_on_one_value(val_1):
        print(val_1)

    # GROUP
    @staticmethod
    def check_group(self):
        reg = re.split(r"\s{2,}", self)  # multidimensional list
        find = re.search(',', reg[2])
        if find:
            table_split = reg[2].replace(',', ' ').replace('-', ' ').split()
            if table_split:
                if len(table_split) > 4:
                    return table_split[-3].lstrip('0')
                else:
                    return table_split[1].lstrip('0')
            else:
                return int(reg[2][0:2].lstrip('0'))

    # change to integer
    @staticmethod
    def is_integer(self):
        if self:
            try:
                integer = int(self)
                if integer == 0:
                    return None
                else:
                    return integer
            except ValueError:
                try:
                    str_split = self.split(',')
                    if str_split[0] == 0:
                        return None
                    else:
                        return int(str_split[0])
                except ValueError:
                    return None
        else:
            return None

    # change to float
    @staticmethod
    def is_float(self):
        try:
            float_self = float(self.replace(',', '.'))
            return float_self
        except ValueError:
            return 0.00

    # get VAT
    @staticmethod
    def get_VAT():
        xlsx_path = 'resources/import/TVA.xlsx'  # Xlsx file path
        data = get_data(xlsx_path, start_row=1)

        # VAT
        for row in data['TVA']:
            try:
                if row:
                    Article.objects.filter(code_article=row[0]).update(taux_TVA=row[1])

            except Article.DoesNotExist as e:
                print('ERROR VAT', e)
                raise e
        print('vat creation done')

    # Insert in DB
    @staticmethod
    def insert_into_db(self):
        f = open('resources/erreurs/articles_tri_erreurs.txt', 'w')
        f_delete = open('resources/del_articles.txt', 'w')
        f_art_err = open('resources/erreurs/articles_non_insérés.txt', 'w')
        for rst in self:
            # Families
            if os.path.isfile('resources/famille/famille_' + str(rst['famille']) + '.txt'):
                file = open('resources/famille/famille_' + str(rst['famille']) + '.txt', 'a')
                files = open('resources/famille/famille_' + str(rst['famille']) + '.txt', 'r')
                strings = files.read()
                if not str(rst['groupe']) in strings:
                    file.write(str(rst['groupe']))
                    file.write(', ')
                file.close()
            else:
                file = open('resources/famille/famille_' + str(rst['famille']) + '.txt', 'w')
                file.write(str(rst['groupe']))
                file.write(', ')
                file.close()

            # SubFamilies
            if os.path.isfile('resources/sousfamille/sousfamille_' + str(rst['sous_famille']) + '.txt'):
                file = open('resources/sousfamille/sousfamille_' + str(rst['sous_famille']) + '.txt', 'a')
                files = open('resources/sousfamille/sousfamille_' + str(rst['sous_famille']) + '.txt', 'r')
                strings = files.read()
                if not str(rst['famille']) in strings:
                    file.write(str(rst['famille']))
                    file.write(', ')
                file.close()
            else:
                file = open('resources/sousfamille/sousfamille_' + str(rst['sous_famille']) + '.txt', 'w')
                file.write(str(rst['famille']))
                file.write(', ')
                file.close()

            # Check if no null
            if rst["groupe"] is not None or rst["famille"] is not None or rst["sous_famille"] is not None:

                # ManyToOne -> get or null
                try:
                    group = Groupe.objects.get(id=rst["groupe"])
                except Groupe.DoesNotExist:
                    group = None

                try:
                    family = Famille.objects.get(id=rst["famille"])
                except Famille.DoesNotExist:
                    family = None

                try:
                    subfamily = SousFamille.objects.get(id=rst["sous_famille"])
                except SousFamille.DoesNotExist:
                    subfamily = None
                    print('coucou')
                if rst['prix_achat_1'] > 0.00 or rst['prix_achat_2'] > 0.00 or rst['prix_achat_3'] > 0.00 or rst['prix_achat_4'] > 0.00 or rst['code_article'] != 'AAAA01' or rst['code_article'] is not 'AAAA02':
                    print('>0.00')
                    try:
                        print('test')
                        Article.objects.update_or_create(
                                code_article=rst["code_article"],
                                gencode=rst["gencode"],

                                defaults=dict(
                                    libelle=rst['libelle'],
                                    prix_vente=rst["prix_vente"],
                                    prix_achat_1=rst["prix_achat_1"],
                                    prix_achat_2=rst["prix_achat_2"],
                                    prix_achat_3=rst["prix_achat_3"],
                                    prix_achat_4=rst["prix_achat_4"],
                                    conditionnement=rst["conditionnement"],
                                    groupe=group,
                                    famille=family,
                                    sous_famille=subfamily,
                                )

                            )
                        print('inserted', rst['libelle'])
                    except Exception as err:
                        f_art_err.write('not inserted ' + rst['code_article'] + '\n')
                        print('not inserted', rst['code_article'])
                        print(err)
                        raise err

                else:
                    print('===0.00')
                    try:
                        article = Article.objects.get(
                            code_article=rst["code_article"],
                            gencode=rst["gencode"], )
                        article.delete()
                        f_delete.write('delete ' + rst['code_article'] + '\n')
                    except ObjectDoesNotExist:
                        pass

            else:
                f.write(rst['code_article'] + '\n')

        f_art_err.close()
        f.close()
