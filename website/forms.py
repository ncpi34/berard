from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from website.models import Article


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d 'utilisateur", max_length=200)
    # telephone = forms.CharField(label="N° client", max_length=200)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)



