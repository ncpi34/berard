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
from website.models import Article, Groupe, ProfilUtilisateur, HistoriqueCommande
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.cache import cache_page
import time
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings

""" login"""


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', locals())

    def post(self, request):
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                try:
                    user = User.objects.get(username=username, password=password)
                    try:
                        tarif = user.profilutilisateur.tarif
                        # user = authenticate(username=username, password=password)
                        # admin = User.objects.filter(username=username, groups__name='admin')  # Check if admin
                        if user and tarif:
                            if tarif is not '0':
                                # messages.success(request, 'Vous êtes bien connecté')
                                login(request, user)
                                request.session['tarif'] = int(user.profilutilisateur.tarif)
                                return redirect('website:products')
                                # return HttpResponse("Vous avez été redirigé.")
                        else:
                            messages.error(request, 'Vos identifiants sont erronés')
                            return render(request, 'auth/login.html', locals())

                    except ProfilUtilisateur.DoesNotExist:
                        messages.error(request, "Vous n'avez pas accès à ce site")
                        return render(request, 'auth/login.html', locals())

                except User.DoesNotExist:
                    messages.error(request, "Vous n'avez pas de compte")
                    return render(request, 'auth/login.html', locals())


def logout_view(request):
    logout(request)
    return redirect('website:login')


""" Products views"""


class ArticleView(LoginRequiredMixin, ListView, SuccessMessageMixin):
    template_name = 'website/products.html'
    paginate_by = 60
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''
    success_message = 'List successfully saved!!!!'

    def get_queryset(self):
        if self.request.GET.get('code_article'):
            query = self.request.GET.get('code_article')
            postresult = Article.objects.filter(Q(actif=True) & Q(code_article__contains=query)
                                                | Q(actif=True) & Q(libelle__contains=query.upper()))
            return postresult
        elif self.kwargs.get('group') and self.kwargs.get('family') and not self.request.GET.get('code_article'):
            _family = self.kwargs.get("family")
            _group = self.kwargs.get("group")
            article = Article.objects.filter(
                Q(actif=True)
                & Q(groupe__nom=_group)
                & Q(famille__nom=_family)).exclude(Q(prix_achat_1=0.00)
                                                   )
            return article
        elif self.kwargs.get('group'):
            _name = self.kwargs.get("group")
            article = Article.objects.filter(Q(actif=True) & Q(groupe__nom=_name)).exclude(Q(prix_achat_1=0.00))
            return article

        elif self.kwargs.get('subfamily'):
            _name = self.kwargs.get("subfamily")
            article = Article.objects.filter(Q(actif=True) & Q(sous_famille__nom=_name)).exclude(Q(prix_achat_1=0.00))
            return article

        else:
            if not settings.CONNECTED_OR_NOT:
                messages.info(self.request, 'Bienvenue ' + self.request.user.last_name)
                settings.CONNECTED_OR_NOT = True
            article = Article.objects.filter(Q(actif=True)).exclude(Q(prix_achat_1=0.00))
            return article

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        context['filter'] = ArticleFilter()
        return context

    # def get_success_url(self):
    #     messages.success(self.request, "deleted successfully")
    #     return reverse("/")


class ArticleByFamillyView(LoginRequiredMixin, ListView):
    template_name = 'website/products.html'
    paginate_by = 60
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''

    def get_queryset(self):
        print('FAMILYYYYYY')
        print(self.request.GET.get('code_article'))
        _name = self.kwargs.get("nom")
        article = Article.objects.filter(Q(famille__nom=_name))
        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleByFamillyView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'website/product.html'
    queryset = Article.objects.all()
    login_url = ''

    def get_object(self):
        id_ = self.kwargs.get('pk')
        # article.nb_vues += 1  # views_numb
        # article.save()
        return get_object_or_404(Article, pk=id_)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


"""Order Summary"""


class OrderSummaryView(LoginRequiredMixin, ListView):
    template_name = 'website/order_summary/order_summary.html'
    queryset = HistoriqueCommande.objects.all()
    login_url = ''
    context_object_name = 'histories'

    def get_queryset(self):
        _user = self.request.user.id
        history = HistoriqueCommande.objects.filter(Q(utilisateur__id=_user)).order_by('-date')[:4]
        return history


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'website/order_summary/order_detail.html'
    queryset = HistoriqueCommande.objects.all()
    login_url = ''

    # context_object_name = 'article'

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(HistoriqueCommande, pk=id_)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
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
