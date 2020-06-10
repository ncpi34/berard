import factory

from tests.factories.famille import FamilleFactory
from tests.factories.groupe import GroupeFactory
from website.models import Groupe, Famille


class ArticleFactory(factory.django.DjangoModelFactory):
    code_article = factory.Sequence(lambda n: "art_ %03d" % n)
    libelle = factory.Sequence(lambda n: "libellé %03d" % n)
    conditionnement = factory.Sequence(lambda n: "cdt par %03d" % n)
    prix_vente = 10.00
    prix_achat_1 = 16.00
    prix_achat_2 = 17.00
    prix_achat_3 = 18.00
    prix_achat_4 = 19.00
    gencode = 'AAA120546'
    taux_TVA = 20
    groupe = factory.Iterator(Groupe.objects.all())
    famille = factory.Iterator(Famille.objects.all())
    # groupe = factory.SubFactory(GroupeFactory)
    # famille = factory.SubFactory(FamilleFactory)
    image = 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.planet-product.com%2F160-home_default%2Fargan-cooking-oil.jpg&imgrefurl=https%3A%2F%2Fwww.planet-product.com%2Fen%2F5-alimentary&tbnid=00D6Lu2d0U0UvM&vet=12ahUKEwj88vbZ_-LpAhVLZRoKHROUAMwQMygJegUIARD6AQ..i&docid=iRm0ynY7nyjVwM&w=275&h=349&q=image%20product%20alimentary&ved=2ahUKEwj88vbZ_-LpAhVLZRoKHROUAMwQMygJegUIARD6AQ'

    class Meta:
        model = 'website.Article'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('code_article', 'libelle', 'conditionnement',
                                'prix_vente', 'prix_achat', 'gencode',
                                'taux_TVA', 'groupe', 'famille')
