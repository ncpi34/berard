import json
from django.contrib.auth.models import User
from django.http import HttpResponse
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
                    group = Groupe.objects.update_or_create(nom=row[1], )
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
        self = cls()
        data = get_data(self.xlsx_path, start_row=1)

        # Groupe
        for row in data['Groupe']:
            print(row[1])
            try:
                # group = Groupe.objects.update_or_create(nom=row[1], )
                group = Groupe(nom=row[1], pk=row[0])
                group.save()
            except Exception as e:
                print('group_creation')
                print(e)
                raise e
        print('groupe creation done')

        # FAMILY
        for row in data['Famille']:
            print(row[1])
            try:
                int(row[0])
                print('Groupe_id', row[0])
                group = Groupe.objects.get(id=int(row[0]))
                print('GROUP', group)
                family = Famille.objects.update_or_create(nom=row[1],
                                                          pk=row[2],
                                                          groupe=group)
            except ValueError:
                family = Famille.objects.update_or_create(nom=row[1],
                                                          pk=row[2],
                                                          groupe=None)

            except Exception as e:
                print('family_creation_error')
                print(e)
                raise e
        print('family creation done')

        # SUBFAMILY
        for row in data['SousFamille']:
            print(row[1])
            try:
                int(row[0])
                family = Famille.objects.get(id=int(row[0]))
                print('FAMILY', family)
                sub_family = SousFamille.objects.update_or_create(nom=row[1],
                                                                  pk=row[2],
                                                                  famille=family)

            except ValueError:
                sub_family = SousFamille.objects.update_or_create(nom=row[1],
                                                                  pk=row[2],
                                                                  famille=None)

            except Exception as e:
                print('subfamily_creation_error')
                print(e)
                raise e
        print('subfamily creation done')

        # resp = json.dumps(csv_reader)
        return HttpResponse(request, content_type='application/json')
