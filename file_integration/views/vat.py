import os
from django.http import HttpResponse
from file_integration.connect_to_ftp import connect_ftp
from website.models import Article
import os.path
from pyexcel_xlsx import get_data
import xlsxwriter


class VatViews(object):
    @classmethod
    def file_treatement(cls, request, **kwargs):
        if kwargs['password'] == 'berard_vat':
            path_server = 'resources/import/'
            if not os.path.exists(path_server):
                os.makedirs(path_server)
            response = cls.get_VAT()  # insert VAT from an other file
            # cls.del_article_not_in_txt(array_of_obj) # clean db
            # cls.check_picture()  # to check pictures
            if response:
                return HttpResponse(200, content_type='application/json')
            return HttpResponse(500, content_type='application/json')



    @staticmethod
    def check_picture():
        articles = Article.objects.all()
        workbook = xlsxwriter.Workbook('photo.xlsx')
        worksheet = workbook.add_worksheet()

        # Some data we want to write to the worksheet.
        expenses = (
            ['Rent', 1000],
            ['Gas', 100],
            ['Food', 300],
            ['Gym', 50],
        )

        # Start from the first cell. Rows and columns are zero indexed.
        row = 1
        col = 0

        # headers
        worksheet.write(0, 0, 'Libelle')
        worksheet.write(0, 1, 'code')
        worksheet.write(0, 2, 'gencod')
        worksheet.write(0, 3, 'rayon')
        worksheet.write(0, 4, 'famille')

        # Iterate over the data and write it out row by row.
        for item in articles:
            if not os.path.exists(f"D:\Projets\Berard\media\img\product\{item.code_article}.jpg"):
                worksheet.write(row, col, item.libelle)
                worksheet.write(row, col + 1, item.code_article)
                worksheet.write(row, col + 2, item.gencode)
                if item.groupe is not None:
                    worksheet.write(row, col + 3, item.groupe.nom)
                if item.famille is not None:
                    worksheet.write(row, col + 4, item.famille.nom)
                # worksheet.write(row, col + 1, cost)
                row += 1

        # Write a total using a formula.
        worksheet.write(row, 0, 'Total')
        worksheet.write(row, 1, f'{row - 1}')

        workbook.close()

        # for article in articles:
        #     print(article)
        # os.path.exists("file.txt")
        return True

    @staticmethod
    def del_article_not_in_txt(arr_obj):
        f_delete = open('resources/del_articles.txt', 'w')
        articles = Article.objects.all()
        x = 0
        result = False
        while x < articles.count():
            for item in arr_obj:
                if articles[x].code_article is item["code_article"]:
                    result = True
                    break
                else:
                    pass
                    # art.delete()

            if not result:
                f_delete.write('delete ' + articles[x].code_article + '\n')
                articles[x].delete()
            else:
                print('not deleted', articles[x].code_article)

            x += 1
        f_delete.close()
        return True

    @staticmethod
    def get_VAT():
        path_server = 'resources/import/'
        if not os.path.exists(path_server):
            os.makedirs(path_server)

        path_ftp = '/SiteWeb/tva_produits'
        f = "TVA.xlsx"
        ftp = connect_ftp(path_server, path_ftp, f)
        if ftp:
            try:
                data = get_data(os.path.join(path_server, f), start_row=1)
                for row in data['TVA']:
                    try:
                        if row:
                            Article.objects.filter(code_article=row[0]).update(taux_TVA=row[1])
                            print('vat ok')
                    except Article.DoesNotExist as e:
                        print('ERROR VAT', e)
                        raise e
                print('vat creation done')
                return True
            except OSError as error:
                print("OS error: {0}".format(error))
                return False


