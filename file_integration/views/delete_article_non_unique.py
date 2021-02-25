import os
from django.http import HttpResponse
from file_integration.connect_to_ftp import connect_ftp
from website.models import Article
import os.path
from pyexcel_xlsx import get_data
import xlsxwriter


class DeleteDoubleArticleViews(object):
    @classmethod
    def file_treatement(cls, request, **kwargs):
        if kwargs['password'] == 'art_non_unq':
            path_server = 'resources/import/'
            if not os.path.exists(path_server):
                os.makedirs(path_server)
            response = cls.delete_non_unique()  # insert VAT from an other file
            # cls.del_article_not_in_txt(array_of_obj) # clean db
            # cls.check_picture()  # to check pictures
            if response:
                return HttpResponse(200, content_type='application/json')
            return HttpResponse(500, content_type='application/json')

    @staticmethod
    def delete_non_unique():
        try:
            Article.objects.all().delete()
            return True
        except:
            return False
        # path_server = 'resources/import/'
        # if not os.path.exists(path_server):
        #     os.makedirs(path_server)
        #
        # path_ftp = '/SiteWeb/tva_produits'
        # f = "TVA.xlsx"
        # ftp = connect_ftp(path_server, path_ftp, f)
        # if ftp:
        #     try:
        #         data = get_data(os.path.join(path_server, f), start_row=1)
        #         for row in data['TVA']:
        #             try:
        #                 if row:
        #                     article = Article.objects.filter(code_article=row[0])
        #                     if article.count() > 1:
        #                         article
        #                     print('count: ', article.count())
        #                     print('vat ok')
        #             except Article.DoesNotExist as e:
        #                 print('ERROR UNQ', e)
        #                 raise e
        #         print('vat creation done')
        #         return True
        #     except OSError as error:
        #         print("OS error: {0}".format(error))
        #         return False
