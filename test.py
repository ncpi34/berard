import re
from ftplib import FTP
import os
import string
import numpy as np

import json
from django.http import HttpResponse
from django.shortcuts import render
from website.models import Article, Groupe, Famille, SousFamille
import os.path

""" Article File"""


class ArticleAutomate:
    # Check errors
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

    # Insert in DB
    @staticmethod
    def insert_into_db(self):
        f = open('resources/erreurs/articles_tri_erreurs.txt', 'w')
        f_art_err = open('resources/erreurs/articles_non_insérés.txt', 'w')

        for rst in self:

            # Families
            if os.path.isfile('resources/famille/famille_' + str(rst['famille']) + '.txt'):
                file = open('resources/famille/famille_' + str(rst['famille']) + '.txt', 'a')
                files = open('resources/famille/famille_' + str(rst['famille']) + '.txt', 'r')
                strings = files.read()
                if str(rst['groupe']) in strings:
                    file.close()
                else:
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
                if str(rst['famille']) in strings:
                    file.close()
                else:
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
                print(rst['libelle'])

                # ManyToOne
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

                try:


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
                        groupe=group,
                        famille=family,
                        sous_famille=subfamily,
                    )
                    print('inserted')

                except Exception as err:
                    f_art_err.write('not inserted ' + rst['code_article'] + '\n')
                    print('not inserted', rst['code_article'])
                    print(err)
                    raise err
            else:
                f.write(rst['code_article'] + '\n')

        f_art_err.close()
        f.close()

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
            ftp.retrbinary('RETR TART.PLN', open(os.path.join(path, 'TART.PLN'), 'wb').write)
            ftp.quit()

            with open(os.path.join(path, 'TART.PLN'), encoding="utf-8", errors='ignore') as file:
                text_lines = file.readlines()

            # array of dict
            obj_bdd = [{
                "code_article": val[10:16],
                "libelle": val[18:54],
                "conditionnement": cls.is_integer(val[54:58]),

                "prix_achat_1": cls.is_float(val[83:91]),
                "prix_achat_2": cls.is_float(val[91:99]),
                "prix_achat_3": cls.is_float(val[99:107]),
                "prix_achat_4": cls.is_float(val[107:115]),
                "prix_vente": cls.is_float(val[161:169]),

                "gencode": val[228:241],
                # # "taux_TVA": 6,  # TO DEFINE

                "tri": val[58:68],
                "groupe": cls.is_integer(val[58:60]),
                # "famille": cls.is_integer(val[62:64]),
                "famille": cls.is_integer(val[61:64]),
                "sous_famille": cls.is_integer(val[65:68]),
            } for val in text_lines]

            f = open('tri.txt', 'w')
            [f.write(i['tri'] + '\n') for i in obj_bdd]
            f.close()

            # print([i['tri'] for i in obj_bdd])

            cls.insert_into_db(obj_bdd)  # call method to insert in db
            file.close()
            resp = json.dumps(obj_bdd)
            return True

        except OSError as error:
            print("OS error: {0}".format(error))
            return False