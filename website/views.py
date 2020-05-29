from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from website.forms import LoginForm
from website.models import Article

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
    template_name = 'home.html'
    login_url = ''

    def get_queryset(self):
        return Article.objects.all()
        # return Article.objects.all().order_by('libelle')[0:50]

