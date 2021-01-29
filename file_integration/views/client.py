import os
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from file_integration.connect_to_ftp import connect_ftp


class ClientViews(object):
    """
    Client File
    """
    @staticmethod
    def test_crontab():
        with open("test_crontab.txt", "w") as f:
            f.write('Hello World')

    @classmethod
    def file_treatement(cls, request, **kwargs):
        if kwargs['password'] == 'berard_client':
            cls.test_crontab()
            path_server = 'resources/import/'
            if not os.path.exists(path_server):
                os.makedirs(path_server)

            path_ftp = '/Rep/EXPORT'
            f = "TCLT.PLN"
            ftp = connect_ftp(path_server, path_ftp, f)
            if ftp:
                try:

                    with open(os.path.join(path_server, f), encoding='utf-8', errors='ignore') as file:
                        text_lines = file.readlines()

                    array_of_obj = cls.build_array(text_lines)
                    cls.insert_into_db(array_of_obj)  # call method to insert in db

                    file.close()
                    print('done client')
                    return HttpResponse(200, content_type='application/json')

                except Exception as error:
                    raise error

        else:
            return HttpResponseBadRequest("Vous n'avez pas les accés")

    @classmethod
    def build_array(cls, array):
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

        } for val in array]
        return obj_bdd

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
                print(rst["code_client"], " done")
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
