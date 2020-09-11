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
  

    # def clean(self):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #     user = User.objects.filter(username=username, password=password)
    #     if not user:
    #         raise forms.ValidationError("Vous n'avez pas de compte")
    #     return username

    # def clean(self):
    #     cleaned_data = super(ContactForm, self).clean()
    #     sujet = cleaned_data.get('sujet')
    #     message = cleaned_data.get('message')
    #
    #     if sujet and message:  # Est-ce que sujet et message sont valides ?
    #         if "pizza" in sujet and "pizza" in message:
    #             raise forms.ValidationError(
    #                 "Vous parlez de pizzas dans le sujet ET le message ? Non mais ho !"
    #             )
    #             self.add_error("message",
    #                            "Vous parlez déjà de pizzas dans le sujet, "
    #                            "n'en parlez plus dans le message !"
    #                            )
    #
    #     return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK
