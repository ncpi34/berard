import json
from django.contrib.auth.models import User
from django.http import HttpResponse
import io
import csv

from website.models import Groupe, Famille

"""Groups Families and Sub-Families"""


class Familly(object):

    @classmethod
    def create_families(cls):



        CSV_PATH = 'D:\Société Berard\GROUPE FAMILLE SOUS FAMILLE\famille.csv'  # Csv file path

        with open(CSV_PATH, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar=';')
            for column in spamreader:
                try:
                    familly = Famille(nom=column[1],)

                    # You have to save the object before adding the m2m relations
                    familly.save()
                    familly.groupe.add(column[2])  #
                    # group = Group.objects.get(name='user')
                    # user.groups.set([group])  # groups MtM

                except Exception as e:
                    raise e

        return 'something'

        # resp = json.dumps(obj_bdd)
        # return HttpResponse(resp, content_type='application/json')
