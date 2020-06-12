import json
from django.http import HttpResponse
import io
import csv

from website.models import Famille, SousFamille


class SubFamilyViews(object):
    @classmethod
    def create_sub_family(cls, request):

        csv_path = 'D:\Société Berard\GROUPE FAMILLE SOUS FAMILLE\sous_famille.csv'  # Csv file path

        with open(csv_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar=';')
            next(csv_reader)
            for row in csv_reader:
                try:
                    print(int(row[2]))
                    family = Famille.objects.get(id=int(row[2]))
                    print(family)
                    sub_family = SousFamille(nom=row[1],
                                             famille=family)
                    #
                    # # You have to save the object before adding the m2m relations
                    sub_family.save()

                except Exception as e:
                    raise e

        # resp = json.dumps(obj_bdd)
        return HttpResponse(request, content_type='application/json')
