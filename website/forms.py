from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from website.models import Article


class ForgotPassForm(forms.Form):
    email = forms.CharField(label="Entrez votre adresse email svp", max_length=200,
                            widget=forms.EmailInput(
                                # attrs={'style': 'text-align:center',
                                #        }
                            )
                            )


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d 'utilisateur", max_length=200,
                               widget=forms.TextInput(
                                   attrs={
                                    #    'style': 'text-align:center',
                                          'id':'username'
                                    }
                               )
                               )
   
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput(
                                       attrs={
                                        #    'style': 'max-width:50%',
                                           'id':'password'
                                              }
                               )
                               )
