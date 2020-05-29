import factory

from tests.factories.famille import FamilleFactory
from tests.factories.groupe import GroupeFactory


class ArticleFactory(factory.django.DjangoModelFactory):
    code_article = factory.Sequence(lambda n: "art_ %03d" % n)
    libelle = factory.Sequence(lambda n: "libellé %03d" % n)
    conditionnement = factory.Sequence(lambda n: "cdt par %03d" % n)
    prix_vente = 10.00
    prix_achat = 15.00
    gencode = 120354
    taux_TVA = 20
    groupe = factory.SubFactory(GroupeFactory)
    famille = factory.SubFactory(FamilleFactory)
    image = 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.monoprix.fr%2Fassets%2Fimages%2Fgrocery%2F3341719' \
            '%2F580x580.jpg%3Fimpolicy%3DHigh_Grocery&imgrefurl=https%3A%2F%2Fwww.monoprix.fr%2Fcourses%2Fcocacola' \
            '-coca-cola-3341719-p&tbnid=5zea_gEfUi0v-M&vet=12ahUKEwi0543M_NjpAhXH_IUKHevsAy8QMygAegUIARCIAg..i&docid' \
            '=brOSLKt23baLXM&w=580&h=580&q=image%20coca%20cola&ved=2ahUKEwi0543M_NjpAhXH_IUKHevsAy8QMygAegUIARCIAg '

    class Meta:
        model = 'website.Article'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('code_article', 'libelle', 'conditionnement',
                                'prix_vente', 'prix_achat', 'gencode',
                                'taux_TVA', 'groupe', 'famille')
