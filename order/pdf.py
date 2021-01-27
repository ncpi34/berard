from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from order.models import ProduitCommande
from website.models import Article
from order.models import HistoriqueCommande
import io
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import re

""" Pdf Generation """

PAGESIZE = A4
BASE_MARGIN = 10 * mm
style_right = ParagraphStyle(name='right', parent=getSampleStyleSheet()['Normal'], alignment=TA_RIGHT)
style_left = ParagraphStyle(name='left', parent=getSampleStyleSheet()['Normal'], alignment=TA_LEFT)


class PdfCreator(object):

    @staticmethod
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "%d" % doc.page
        canvas.drawCentredString(
            0.75 * inch,
            0.75 * inch,
            page_number_text
        )
        canvas.restoreState()

    @staticmethod
    def get_title_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['BodyText']
        body_style.fontSize = 10
        return body_style

    @staticmethod
    def get_body_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['Heading1']
        body_style.fontSize = 12
        body_style.fonName = 'Helvetica'
        body_style.alignment = TA_CENTER
        body_style.spaceAfter = 40
        body_style.spaceBefore = -40
        body_style.textColor = colors.black
        return body_style

    @staticmethod
    def get_footer_style_first_elem():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['BodyText']
        body_style.fontSize = 12
        body_style.fonName = 'Helvetica'
        body_style.alignment = TA_CENTER
        # body_style.spaceAfter = 40
        body_style.spaceBefore = 20
        body_style.textColor = colors.black
        return body_style

    @staticmethod
    def get_footer_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['BodyText']
        body_style.fontSize = 8
        body_style.fonName = 'Helvetica'
        body_style.alignment = TA_CENTER
        # body_style.spaceAfter = 40
        body_style.spaceBefore = 10
        body_style.textColor = colors.black
        return body_style

    @staticmethod
    def get_products(order_id):
        products = ProduitCommande.objects.filter(commande__id=order_id)
        tab = []
        for item in products:
            product = get_object_or_404(Article, id=item.article.id)
            table = [product.code_article, product.libelle, item.prix_HT, item.quantite, item.get_cost_without_taxes(), ]
            tab.append(table)
        tab.insert(0, ['Code article', 'Libellé', 'PU HT', 'Quantité', 'Prix HT'])
        return tab

    @staticmethod
    def getinfo_from_user(request):
        user = User.objects.get(id=request.user.id)
        obj = [
            Paragraph(f"Code client: {user.profilutilisateur.code_client}", style_right),
            Paragraph(f"{user.last_name} {user.first_name}", style_right),
            Paragraph(f"{user.profilutilisateur.adresse}", style_right)
        ]
        return obj

    @staticmethod
    def change_hour(date):
        test = list(str(date))
        hour = "".join(test[-21:-19])
        hour.split()
        rst_hour = int(hour) + 2
        str1 = str(rst_hour)
        test[-21] = str1[0]
        test[-20] = str1[1]
        join_list = "".join(test)
        return join_list[0:19]

    @classmethod
    def build_pdf(cls, request, **kwargs):
        order = HistoriqueCommande.objects.get(id=int(kwargs['order_id']))
        date = str(order.date)[0:10]  # date splited

        file_name = re.sub(r'-|:|\s', r'', cls.change_hour(order.date)) + '.pdf'  # name of the file

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=PAGESIZE,
            topMargin=BASE_MARGIN,
            leftMargin=BASE_MARGIN,
            rightMargin=BASE_MARGIN,
            bottomMargin=BASE_MARGIN
        )

        data = cls.get_products(int(kwargs['order_id']))

        logo = Image('media/img/logo-berard-distribution.png')
        logo.drawHeight = 1 * inch
        logo.drawWidth = 2.5 * inch

        body_style = cls.get_body_style()
        title_style = cls.get_title_style()
        footer_style = cls.get_footer_style()
        title_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('VALIGN', (0, 0), (-1, -1), 'TOP')])
        body_table_style = TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
        story = [
            logo,
            Table([
                [
                    [
                        Paragraph("A.R DE COMMANDE N° {}".format(order.id), style_left),
                     ],
                    cls.getinfo_from_user(request)
                ],
            ],
                rowHeights=[1 * inch], style=title_table_style),

            Paragraph(f'Commande du {date}', body_style),

            Table(cls.get_products(order.pk), rowHeights=15 * mm, style=body_table_style),
            Table([[Paragraph("    ")]]),
            Table([
                [
                    [Paragraph("Total HT:    {}€".format(order.get_total_cost_without_taxes()), title_style)],
                    [Paragraph("Total Taxes:    {}€".format(order.get_total_taxes()), title_style)],
                    [Paragraph("Total TTC:    {}€".format(order.get_total_cost_with_taxes()), title_style)],
                ]
            ],
                colWidths=[1 * inch, 1 * inch, 1 * inch],
                rowHeights=[3 * inch], style=title_table_style),
            Paragraph("Berard Distribution - 480 Allée Des Cabedans, 84300 Cavaillon - Tél.: 04 90 71 55 74 ", footer_style)
        ]

        doc.build(
            story,
            onFirstPage=cls.add_page_number,
            onLaterPages=cls.add_page_number,
        )

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response.write(buffer.getvalue())
        buffer.close()
        return response
