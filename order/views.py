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

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(HistoriqueCommande, pk=id_)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        return context

