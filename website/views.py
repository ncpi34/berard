# from bootstrap_modal_forms.generic import BSModalReadView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from cart.forms import CartAddProductForm
from website.filters import ArticleFilter
from website.forms import LoginForm
from website.models import Article, Groupe
from django.db.models import Q

""" login"""


def login_view(request):
    error = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            # admin = User.objects.filter(username=username, groups__name='admin')  # Check if admin
            if user:
                messages.success(request, 'Vous êtes bien connecté')
                login(request, user)
                return redirect('/home')
            else:
                messages.error(request, 'Vos identifiants sont erronés')
                error = True
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', locals())


def logout_view(request):
    logout(request)
    return redirect(reverse(login_view))


""" Products views"""


class ArticleView(LoginRequiredMixin, ListView):

    template_name = 'website/products.html'
    # template_name = 'home.html'
    # queryset = Article.objects.filter(actif=False)
    paginate_by = 50
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''

    def get_queryset(self):
        if self.kwargs.get('nom'):
            print(self.kwargs.get('nom'))
            _name = self.kwargs.get("nom")
            article = Article.objects.filter(Q(famille__nom=_name))
            # article = ArticleFilter(queryset=_name)
            return article
        elif self.request.GET.get('code_article'):
            print('coucou')
            print(self.request.GET.get('code_article'))
            query = self.request.GET.get('code_article')
            postresult = Article.objects.filter(Q(code_article__contains=query))
            result = postresult
            return result
        # else:
        #     result = None
        # return result
        else:
            article = Article.objects.filter(actif=False)
            # article = Article.objects.filter(actif=True).order_by('libelle')[0:50]
            return article


    # qs = self.model.objects.all()
    # product_filtered_list = ProductFilter(self.request.GET, queryset=qs)
    # return product_filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        context['filter'] = ArticleFilter()
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'website/product.html'
    queryset = Article.objects.all()
    login_url = ''

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=id_)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


class SearchView(ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Article.objects.filter(libelle=query)
            result = postresult
        else:
            result = None
        return result


# class BookReadView(BSModalReadView):
#     model = Article
#     template_name = 'website/display_picture.html'
