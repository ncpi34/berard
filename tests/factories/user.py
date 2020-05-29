import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'website.ProfilUtilisateur'
        django_get_or_create = ('username',)

    telephone = '0604128827'
