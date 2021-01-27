from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from order.models import HistoriqueCommande
from django.db.models import Q


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

