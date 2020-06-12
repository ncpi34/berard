import json
from django.contrib.auth.models import User
from django.http import HttpResponse
import io
import csv
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

from website.models import Groupe, Famille

""" Groups """


class GroupViews(object):

    @classmethod
    def create_group(cls, request, **kwargs):
        csv_path = 'D:\Société Berard\GROUPE FAMILLE SOUS FAMILLE\groupe.csv'  # Csv file path

        with open(csv_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            csv_reader = xlsx_get(csvfile, column_limit=4)
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
                    # raise e

        # return 'something'

        # resp = json.dumps(csv_reader)
        return HttpResponse(request, content_type='application/json')


