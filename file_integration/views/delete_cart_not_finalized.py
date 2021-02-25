import os
from django.http import HttpResponse

from cart.models import PanierEnCours
from file_integration.connect_to_ftp import connect_ftp
from website.models import Article
import os.path
from pyexcel_xlsx import get_data
import xlsxwriter


class DeleteCartsViews(object):
    @classmethod
    def file_treatement(cls, request, **kwargs):
        response = cls.delete_carts()  # insert VAT from an other file
            # cls.del_article_not_in_txt(array_of_obj) # clean db
            # cls.check_picture()  # to check pictures
        if response:
            return HttpResponse(200, content_type='application/json')
        return HttpResponse(500, content_type='application/json')

    @staticmethod
    def delete_carts():
        try:
            PanierEnCours.objects.all().delete()
            return True
        except:
            return False