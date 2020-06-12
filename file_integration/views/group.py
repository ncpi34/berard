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
        self.csv_path = 'D:\Société Berard\GROUPE FAMILLE SOUS FAMILLE\groupe.csv'  # Csv file path
        self.xlsx_path = 'D:\Société Berard\GROUPE FAMILLE SOUS FAMILLE\groupe.xlsx'  # Xlsx file path

    @classmethod
    def create_group_csv(cls, request, **kwargs):
        self = cls()
        with open(self.csv_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(csv_reader)

            for row in csv_reader:
                try:
                    print(row[1])
                    group = Groupe(nom=row[1], )
                    # # print(group)
                    #
                    # # You have to save the object before adding the m2m relations
                    group.save()

                except Exception as e:
                    print(e)
                    raise e

        # return 'something'

        # resp = json.dumps(csv_reader)
        return HttpResponse(request, content_type='application/json')


    @classmethod
    def create_groupand_others_xlsx(cls, request, **kwargs):
        self = cls()
        data = get_data(self.xlsx_path, start_row=1)

        # Groupe
        for row in data['Groupe']:
            print(row)
            try:
                group = Groupe(nom=row[1], )
                group.save()
            except Exception as e:
                print(e)
                raise e
        # FAMILY
        for row in data['Famille']:
            print(row)
            try:
                group = Groupe.objects.get(id=int(row[0]))
                print(group)
                family = Famille(nom=row[1],
                                 groupe=group)

                # You have to save the object before adding the m2m relations
                family.save()

            except Exception as e:
                raise e
        # FAMILY
        for row in data['SousFamille']:
            print(row)
            try:
                family = Famille.objects.get(id=int(row[0]))
                sub_family = SousFamille(nom=row[1],
                                         famille=family)
                # You have to save the object before adding the m2m relations
                sub_family.save()

            except Exception as e:
                raise e

        # resp = json.dumps(csv_reader)
        return HttpResponse(request, content_type='application/json')


