from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from cart.forms import CartAddProductForm
from website.filters import ArticleFilter
from website.forms import LoginForm, ForgotPassForm
from website.models import Article, Groupe, ProfilUtilisateur, Favori, FavorisClient, Nouveaute, NouveautePhoto
from cart.models import PanierEnCours
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
import pandas as pd


class LoginView(View):

    def get_old_cart(self, *args, **kwargs):
        """ get cart not finalized """
        try:
            old_cart = PanierEnCours.objects.get(utilisateur=self.request.user.id).donnees
            for i in old_cart.copy():
                try:
                    Article.objects.filter(pk=i)
                except Article.DoesNotExist:
                    old_cart.pop(i)

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
                        if user.profilutilisateur.tarif == '0':
                            messages.error(self.request, "Vous n'avez pas accès à ce site")
                            return render(self.request, 'auth/login.html')
                        if user:
                            tarif = user.profilutilisateur.tarif
                            login(self.request, user)
                            self.request.session['tarif'] = int(tarif)
                            self.get_old_cart()
                            messages.success(self.request, 'Bienvenue ' + self.request.user.last_name)
                            return redirect('website:home')
                        else:
                            messages.error(self.request, 'Vos identifiants sont erronés')
                            return render(self.request, 'auth/login.html')

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
    messages.warning(request, 'Vous êtes désormais déconnecté')
    return redirect('website:home')


class HomeView(View):

    def get(self, *args, **kwargs):
        qs_novelties = Nouveaute.objects.all()
        novelties_text = None
        if qs_novelties.exists():
            novelties_text = qs_novelties[0]

        qs_novelties_pic = NouveautePhoto.objects.all()
        novelties_pic = None
        pic_list = []
        if qs_novelties_pic.exists():
            for i in qs_novelties_pic:
                pic_list.append(i)
            novelties_pic = pic_list

        return render(self.request, 'website/home.html',
                      {
                          'novelties': novelties_text,
                          'novelties_pic': novelties_pic
                      })


class OffersView(ListView):
    template_name = 'website/product/offers.html'
    # paginate_by = 60
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''

    def get_queryset(self):
        articles = Favori.objects.all()

        return articles

    def get_context_data(self, **kwargs):
        context = super(OffersView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


class FavoritesView(LoginRequiredMixin, ListView):
    template_name = 'website/product/favorites.html'
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''

    def get_queryset(self):
        articles = FavorisClient.objects.filter(utilisateur=self.request.user).iterator()
        art = []
        obj_from_method_db = []
        for article in articles:
            obj_from_method_db.append(article.format_data())

        # sort by quantity
        df = pd.DataFrame(obj_from_method_db)
        if df.empty:
            return ''
        else:
            df = df.sort_values('quantite')
            sorted_list_of_dicts = df.T.to_dict().values()
            for article in list(sorted_list_of_dicts)[0:20]:  # 20first results
                qs_article = Article.objects.filter(pk=article['pk'])
                if qs_article.exists() and article['price'] > 0:
                    art += qs_article
            return art

    def get_context_data(self, **kwargs):
        context = super(FavoritesView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


class ArticleView(ListView, SuccessMessageMixin):
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
                                              | Q(libelle__contains=query.upper())
                                              ).exclude(Q(prix_achat_1=0.00) | Q(actif=False) | Q(taux_TVA=None))

            return articles
        elif self.kwargs.get('group') and self.kwargs.get('family'):
            _family = self.kwargs.get("family")
            _group = self.kwargs.get("group")
            articles = Article.objects.filter(Q(groupe__pk=_group) & Q(famille__pk=_family)).exclude(
                Q(prix_achat_1=0.00) | Q(actif=False) | Q(taux_TVA=None))
            return articles
        elif self.kwargs.get('group'):
            _name = self.kwargs.get("group")
            articles = Article.objects.filter(Q(groupe__pk=_name)).exclude(
                Q(prix_achat_1=0.00) | Q(actif=False) | Q(taux_TVA=None))
            return articles

        elif self.kwargs.get('subfamily'):
            _name = self.kwargs.get("subfamily")
            articles = Article.objects.filter(Q(sous_famille__pk=_name)).exclude(
                Q(prix_achat_1=0.00) | Q(actif=False) | Q(taux_TVA=None))
            return articles

        else:
            article = Article.objects.all().exclude(Q(prix_achat_1=0.00) | Q(actif=False) | Q(taux_TVA=None))
            return article

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        context['filter'] = ArticleFilter()
        return context


class ArticleDetailView(DetailView):
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
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Vous allez recevoir un email contenant les instructions à suivre')
                    return render(request, 'auth/password_forgot.html', locals())

                except User.DoesNotExist:
                    messages.error(request,
                                   'Nous ne parvenons pas à vous envoyer un email, veuillez contacter Berard '
                                   'distribution')
                    return render(request, 'auth/password_forgot.html', locals())
