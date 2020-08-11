from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from order.models import HistoriqueCommande, ProduitCommande
from berard.settings import EMAIL_HOST_USER
from cart.forms import CartAddProductForm
from website.filters import ArticleFilter
from website.forms import LoginForm, ForgotPassForm
from website.models import Article, Groupe, ProfilUtilisateur, Favori
from order.models import HistoriqueCommande
from cart.models import PanierEnCours
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.cache import cache_page
import time
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.contrib.sessions.models import Session
import asyncio
import io
from django.http import FileResponse

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch, mm, pica, toLength
from reportlab.rl_config import defaultPageSize
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import TopPadder
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

import numpy as np
import re
from datetime import datetime, timedelta
from pytz import timezone

""" Pdf Generation """

PAGESIZE = (140 * mm, 216 * mm)
BASE_MARGIN = 5 * mm


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
        body_style.fontSize = 7
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
    def get_footer_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['Heading1']
        body_style.fontSize = 12
        body_style.fonName = 'Helvetica'
        body_style.alignment = TA_CENTER
        # body_style.spaceAfter = 40
        body_style.spaceBefore = 40
        body_style.textColor = colors.black
        return body_style

    @staticmethod
    def get_products(order_id):
        products = ProduitCommande.objects.filter(commande__id=order_id)
        tab = []
        for item in products:
            product = get_object_or_404(Article, id=item.article.id)
            table = [product.code_article, product.gencode, item.prix, item.quantite, item.get_cost(), ]
            tab.append(table)
        tab.insert(0, ['Code article', 'Gencod', 'P.U.', 'Quantité', 'Prix total'])
        return tab
    @staticmethod
    def getinfo_from_user(request):
        user = User.objects.get(id=request.user.id)
        obj = {'name': user.last_name, 'address': user.profilutilisateur.adresse}
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

        logo = Image('media/img/logo.jpg')
        logo.drawHeight = 0.7 * inch
        logo.drawWidth = 0.7 * inch

        body_style = cls.get_body_style()
        title_style = cls.get_title_style()
        footer_style = cls.get_footer_style()
        title_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('VALIGN', (0, 0), (-1, -1), 'TOP')])
        body_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

        user_informations = cls.getinfo_from_user(request)

        story = [
            Table([
                [[logo], [ Paragraph(user_informations['name'], title_style), Paragraph(user_informations['address'], title_style) ]],
                # [Paragraph('Commande du {}'.format(date), title_style), Paragraph('Informations Berard', title_style)]
            ],
                colWidths=[2.3 * inch, 2.3 * inch],
                rowHeights=[1.5 * inch], style=title_table_style),
            Paragraph('Commande du {}'.format(date), body_style),
            Table(data, style=body_table_style),
            Paragraph("Prix total de la commande: {} €".format(order.get_total_cost()), footer_style),

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
