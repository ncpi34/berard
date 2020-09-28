import json
import re

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
import io
import csv
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

from website.models import Groupe, Famille, SousFamille
from pyexcel_xlsx import get_data
import json

""" Groups """


class GroupViews(object):

    def __init__(self):
        self.csv_path = 'resources/group_family_subfamily/groupe.csv'  # Csv file path
        self.xlsx_path = 'resources/group_family_subfamily/groupe.xlsx'  # Xlsx file path

    @classmethod
    def create_group_csv(cls, request, **kwargs):
        self = cls()
        with open(self.csv_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(csv_reader)

            for row in csv_reader:
                try:
                    print(row[1])
                    group = Groupe.objects.get_or_create(nom=row[1], )
                    # # print(group)
                    #
                    # # You have to save the object before adding the m2m relations
                    # group.save()

                except Exception as e:
                    print(e)
                    raise e

        # return 'something'

        # resp = json.dumps(csv_reader)
        return HttpResponse(request, content_type='application/json')

    @classmethod
    def create_group_and_others_xlsx(cls, request, **kwargs):
        if kwargs['password'] == 'berard_group':
            self = cls()
            data = get_data(self.xlsx_path, start_row=1)

            # Groupe
            for row in data['Groupe']:
                try:
                    Groupe.objects.update_or_create(pk=row[0], defaults=dict(nom=row[1], ordre=row[2]))
                    # group = Groupe(nom=row[1], )
                    # group.save()
                except Exception as e:
                    print('ERROR group_creation', e)
                    raise e
            print('groupe creation done')

            # FAMILY
            for row in data['FamilleMTM']:

                if row[0] is not "":

                    if re.search(',', str(row[0])):
                        tab_str_split = str(row[0]).split(',')
                        Famille.objects.update_or_create(pk=row[2], defaults=dict(nom=row[1].strip()))


                        for item in tab_str_split:
                            group = Groupe.objects.get(id=item)
                            family = Famille.objects.get(nom=row[1].strip(),
                                                         pk=row[2])
                            family.groupe.add(group)

                    elif re.search('.', str(row[0])):
                        tab_str_split = str(row[0]).split('.')
                        print(tab_str_split)
                        Famille.objects.update_or_create(pk=row[2], defaults=dict(nom=row[1].strip()))

                        for item in tab_str_split:
                            group = Groupe.objects.get(id=int(item))
                            family = Famille.objects.get(nom=row[1].strip(),
                                                         pk=row[2])
                            family.groupe.add(group)

                    else:
                        group = Groupe.objects.get(id=row[0])
                        print('GROUP', group)
                        family = Famille.objects.get(nom=row[1].strip(),
                                                     pk=row[2])
                        family.groupe.add(group)
                else:
                    family = Famille.objects.get_or_create(nom=row[1].strip(),
                                                           pk=row[2])
                    print("no value for family")

            print('family creation done')

            # SUBFAMILY
            for row in data['SousFamilleMTM']:

                if row[0] is not "":

                    if re.search(',', str(row[0])):
                        tab_str_split = str(row[0]).split(',')
                        SousFamille.objects.update_or_create(pk=row[2], defaults=dict(nom=row[1].strip()))

                        for item in tab_str_split:
                            family = Famille.objects.get(id=item)
                            subfamily = SousFamille.objects.get(nom=row[1].strip(),
                                                                pk=row[2])
                            subfamily.famille.add(family)

                    elif re.search('.', str(row[0])):
                        tab_str_split = str(row[0]).split('.')
                        print(tab_str_split)
                        SousFamille.objects.update_or_create(pk=row[2], defaults=dict(nom=row[1].strip()))
                        for item in tab_str_split:
                            family = Famille.objects.get(id=int(item))
                            subfamily = SousFamille.objects.get(nom=row[1].strip(),
                                                                pk=row[2])
                            subfamily.famille.add(family)

                    else:
                        family = Famille.objects.get(id=row[0])
                        subfamily = SousFamille.objects.get(nom=row[1].strip(),
                                                            pk=row[2])
                        subfamily.famille.add(family)
                else:
                    subfamily = SousFamille.objects.get_or_create(nom=row[1].strip(),
                                                                  pk=row[2])
                    print("no value for subfamily")

            print('subfamily creation done')

            return HttpResponse(200, content_type='application/json')
        else:
            return HttpResponseBadRequest("Vous n'avez pas les accés")
