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


"""Order Summary"""


class OrderSummaryView(LoginRequiredMixin, ListView):
    template_name = 'order/order_summary.html'
    queryset = HistoriqueCommande.objects.all()
    login_url = ''
    context_object_name = 'histories'

    def get_queryset(self):
        _user = self.request.user.id
        history = HistoriqueCommande.objects.filter(Q(utilisateur__id=_user)).order_by('-date')[:4]
        return history


""" Order Detail """
class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'order/order_detail.html'
    queryset = HistoriqueCommande.objects.all()
    login_url = ''

    # context_object_name = 'article'

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(HistoriqueCommande, pk=id_)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        return context

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
        body_style.fontSize = 16
        return body_style

    @staticmethod
    def get_body_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['Heading1']
        body_style.fontSize = 12
        body_style.fonName = 'Helvetica'
        body_style.alignment = TA_CENTER
        body_style.spaceAfter = 40
        # body_style.spaceBefore = 40
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
        print(tab)
        return tab


    @classmethod
    def build_pdf(cls, request, **kwargs):
        name_file = 'commande' + kwargs['order_id'] + '.pdf' # name of the file

        order = HistoriqueCommande.objects.get(id=int(kwargs['order_id']))
        date = str(order.date)[0:19] # date splited

        buffer = io.BytesIO()


        doc =  SimpleDocTemplate(
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


        story = [
            Table([
                [logo, Paragraph('Berard Distribution', title_style) ],
                # [Paragraph('Commande du {}'.format(date), title_style), Paragraph('Informations Berard', title_style)]
                   ],
                  colWidths=[3.3 * inch, 3.3 * inch, 3.3 * inch],
                  rowHeights=[2.5 * inch], style=title_table_style),
            Paragraph('Commande du {}'.format(date), body_style),
            Table(data, style=body_table_style),
            Paragraph("Prix total de la commande: {} € HT".format(order.get_total_cost()), footer_style),

                 ]

        doc.build(
            story,
            onFirstPage=cls.add_page_number,
            onLaterPages=cls.add_page_number,
        )

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + name_file
        response.write(buffer.getvalue())
        buffer.close()
        return response

