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

from berard.settings import EMAIL_HOST_USER
from cart.forms import CartAddProductForm
from website.filters import ArticleFilter
from website.forms import LoginForm, ForgotPassForm
from website.models import Article, Groupe, ProfilUtilisateur, Favori, FavorisClient
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
import operator
import pandas as pd

""" login"""


class LoginView(View):

    def get_old_cart(self, *args, **kwargs):
        """ get cart not finalized """
        try:
            old_cart = PanierEnCours.objects.get(utilisateur=self.request.user.id).donnees
            self.request.session['cart'] = old_cart
        except PanierEnCours.DoesNotExist:
            pass

    def get(self, *args, **kwargs):
        # form = LoginForm()
        return render(self.request, 'auth/login.html', locals())

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            form = LoginForm(self.request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                try:
                    user = User.objects.get(username=username, password=password)
                    try:
                        tarif = user.profilutilisateur.tarif
                        # user = authenticate(username=username, password=password)
                        # admin = User.objects.filter(username=username, groups__name='admin')  # Check if admin
                        if user:
                            login(self.request, user)
                            self.request.session['tarif'] = int(user.profilutilisateur.tarif)
                            self.get_old_cart()
                            messages.success(self.request, 'Bienvenue ' + self.request.user.last_name)
                            return redirect('website:home')
                        else:
                            messages.error(self.request, 'Vos identifiants sont erronés')
                            return render(self.request, 'auth/login.html')
                        #     if tarif is not '0':
                        #         # messages.success(request, 'Vous êtes bien connecté')
                        #         login(request, user)
                        #         request.session['tarif'] = int(user.profilutilisateur.tarif)
                        #         self.get_old_cart(request)
                        #         return redirect('website:offers')
                        #         # return HttpResponse("Vous avez été redirigé.")
                        # else:
                        #     messages.error(request, 'Vos identifiants sont erronés')
                        #     return render(request, 'auth/login.html', locals())

                    except ProfilUtilisateur.DoesNotExist:
                        messages.error(self.request, "Vous n'avez pas accès à ce site")
                        return render(self.request, 'auth/login.html')

                except User.DoesNotExist:
                    messages.error(self.request, "Vous n'avez pas de compte")
                    return render(self.request, 'auth/login.html')
            else:
                messages.error(self.request, "Veuillez bien remplir les champs demandés")
                return render(self.request, 'auth/login.html')        


""" Logout """


def save_cart_before_logout(request):
    """ Save cart before logout"""
    PanierEnCours.objects.update_or_create(
        utilisateur=int(request.session.get('_auth_user_id')),

        defaults=dict(
            donnees=request.session.get('cart'), )
    )


def logout_view(request):
    save_cart_before_logout(request)
    logout(request)
    return redirect('website:login')

""" Home """
class HomeView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'website/home.html')

"""Offers View"""


class OffersView(LoginRequiredMixin, ListView):
    template_name = 'website/product/offers.html'
    # paginate_by = 60
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''

    def get_queryset(self):
        article = Favori.objects.all().iterator()
        art = []
        for ex in article:
            art += Article.objects.filter(libelle=ex)
        return art

    def get_context_data(self, **kwargs):
        context = super(OffersView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


""" Favorites View """


class FavoritesView(LoginRequiredMixin, ListView):
    template_name = 'website/product/favorites.html'
    # paginate_by = 60
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''

    def get_queryset(self):
        articles = FavorisClient.objects.filter(utilisateur=self.request.user).iterator()
        art = []
        obj_from_method_db = []
        for article in articles:
            obj_from_method_db.append(article.get_20_first_results())

        # sort by quantity
        df = pd.DataFrame(obj_from_method_db)
        if df.empty:
            return ''
        else:
            df = df.sort_values('quantite')
            sorted_list_of_dicts = df.T.to_dict().values()

            for article in list(sorted_list_of_dicts)[0:20]:  # 20first results
                art += Article.objects.filter(libelle=article['libelle'])
            return art

    def get_context_data(self, **kwargs):
        context = super(FavoritesView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


""" Products views"""


class ArticleView(LoginRequiredMixin, ListView, SuccessMessageMixin):
    template_name = 'website/product/products.html'
    paginate_by = 60
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''
    success_message = 'List successfully saved!!!!'

    def get_queryset(self):
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            articles = Article.objects.filter(Q(code_article__contains=query.upper())
                                                |Q(libelle__contains=query.upper())
                                                ).exclude(Q(prix_achat_1=0.00) | Q(actif=False))

            return articles
        elif self.kwargs.get('group') and self.kwargs.get('family'):
            _family = self.kwargs.get("family")
            _group = self.kwargs.get("group")
            articles = Article.objects.filter(Q(groupe__pk=_group) & Q(famille__pk=_family)).exclude(Q(prix_achat_1=0.00) | Q(actif=False))
            return articles
        elif self.kwargs.get('group'):
            _name = self.kwargs.get("group")
            articles = Article.objects.filter(Q(groupe__pk=_name)).exclude(Q(prix_achat_1=0.00) | Q(actif=False))
            return articles

        elif self.kwargs.get('subfamily'):
            _name = self.kwargs.get("subfamily")
            articles = Article.objects.filter(Q(sous_famille__pk=_name)).exclude(Q(prix_achat_1=0.00) | Q(actif=False) )
            return articles

        else:
            article = Article.objects.all().exclude(Q(prix_achat_1=0.00) | Q(actif=False))
            return article

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        context['filter'] = ArticleFilter()
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'website/product/product.html'
    queryset = Article.objects.all()
    login_url = ''

    def get_object(self):
        id_ = self.kwargs.get('pk')
        # views_numb
        article = Article.objects.get(id=id_)
        article.nb_vues += 1
        article.save()
        return get_object_or_404(Article, pk=id_)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


""" Password forgot"""


class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):
        form = ForgotPassForm()
        return render(request, 'auth/password_forgot.html', locals())

    def post(self, request):
        if request.method == "POST":
            form = ForgotPassForm(request.POST)
            if form.is_valid():
                mail = form.cleaned_data['email']
                try:
                    User.objects.get(email=mail)
                    user = User.objects.get(email=mail)
                    send_mail(
                        'Mot de passe oublié',
                        'Votre mot de passe:  ' + user.password,
                        'test34980test@gmail.com',
                        # EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Vous allez recevoir un email contenant les instructions à suivre')
                    # messages.add_message(request, messages.SUCCESS, 'Vous allez recevoir un email contenant les instructions à suivre')
                    # time.sleep(5)
                    # return redirect(reverse('website:login'))
                    return render(request, 'auth/password_forgot.html', locals())

                except User.DoesNotExist:
                    messages.error(request,
                                   'Nous ne parvenons pas à vous envoyer un email, veuillez contacter Berard distribution')
                    return render(request, 'auth/password_forgot.html', locals())
