import re
import os
from django.http import HttpResponse, HttpResponseBadRequest
from file_integration.connect_to_ftp import connect_ftp
from website.models import Article, Groupe, Famille, SousFamille
import os.path
from pyexcel_xlsx import get_data
from django.core.exceptions import ObjectDoesNotExist
import xlsxwriter


class ArticleViews(object):
    """
    Article File
    """

    @classmethod
    def file_treatement(cls, request, **kwargs):
        if kwargs['password'] == 'berard_article':
            path_server = 'resources/import/'
            if not os.path.exists(path_server):
                os.makedirs(path_server)

            path_ftp = '/Rep/EXPORT'
            f = "TART.PLN"
            ftp = connect_ftp(path_server, path_ftp, f)
            if ftp:
                try:

                    with open(os.path.join(path_server, f), encoding="utf-8", errors='ignore') as file:
                        text_lines = file.readlines()

                    array_of_obj = cls.build_array(text_lines)
                    cls.insert_into_db(array_of_obj)  # call method to insert in db

                    file.close()

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
    def get_errors_on_three_values(val_1, val_2, val_3):
        try:
            int(val_1)
        except ValueError:
            try:
                int(val_2)
            except ValueError:
                try:
                    int(val_3)
                except ValueError:
                    print('error on three values')

    # Check errors
    @staticmethod
    def get_error_on_one_value(val_1):
        print(val_1)

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

    @staticmethod
    def is_float(self):
        try:
            float_self = float(self.replace(',', '.'))
            return float_self
        except ValueError:
            return 0.00

    @staticmethod
    def get_VAT():
        path_server = 'resources/import/'
        if not os.path.exists(path_server):
            os.makedirs(path_server)

        path_ftp = '/SiteWeb/tva_produits'
        f = "TVA.xlsx"
        ftp = connect_ftp(path_server, path_ftp, f)
        if ftp:
            try:
                data = get_data(os.path.join(path_server, f), start_row=1)
                for row in data['TVA']:
                    try:
                        if row:
                            Article.objects.filter(code_article=row[0]).update(taux_TVA=row[1])
                            print('vat ok')
                    except Article.DoesNotExist as e:
                        print('ERROR VAT', e)
                        raise e
                print('vat creation done')

            except OSError as error:
                print("OS error: {0}".format(error))
                return False


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
                if rst['prix_achat_1'] > 0.00 or rst['prix_achat_2'] > 0.00 or rst['prix_achat_3'] > 0.00 \
                        or rst['prix_achat_4'] > 0.00 or rst['code_article'] != 'AAAA01' or rst['code_article'] != 'AAAA02':
                    try:

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
                        print(rst["code_article"], " done")

                    except Exception as err:
                        f_art_err.write('not inserted ' + rst['code_article'] + '\n')
                        print('not inserted', rst['code_article'])
                        print(err)
                        raise err

                else:
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

        f_delete.close()
        f_art_err.close()
        f.close()
