import json
from django.http import HttpResponse
import io
import csv

from website.models import Groupe, Famille


class FamilyViews(object):
    @classmethod
    def create_family(cls, request):

        csv_path = 'D:\Société Berard\GROUPE FAMILLE SOUS FAMILLE\Famille.csv'  # Csv file path

        with open(csv_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar=';')
            next(csv_reader)
            for row in csv_reader:
                try:
                    print(int(row[2]))
                    group = Groupe.objects.get(id=int(row[2]))
                    print(group)
                    family = Famille(nom=row[1],
                                     groupe=group)
                    #
                    # # You have to save the object before adding the m2m relations
                    family.save()
                    # familly.groupe.add(row[2])  #
                    # group = Group.objects.get(name='user')
                    # user.groups.set([group])  # groups MtM

                except Exception as e:
                    raise e

        # resp = json.dumps(obj_bdd)
        return HttpResponse(request, content_type='application/json')
