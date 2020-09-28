import itertools
from django.db.models import Q
from website.models import Groupe, Famille, SousFamille

""" Dynamic menus and submenus from DB"""


# to get parent menu
def get_menus(request):
    group_query = Groupe.objects.all().exclude(
        Q(nom__in=['DIVERS', 'BOISSONS BIO', 'ENTRETIEN BIO', 'EPICERIE BIO', 'FRAIS BIO'])
    ).order_by('ordre').values_list('nom', 'pk')
    groups = [list(i) for i in group_query]
    liste = [{"id": item[0][1],
              "name": item[0][0], 'url': '#',  # retrieve query to array of dictionnaries
              'validators': ["menu_generator.validators.is_authenticated"],
              "submenu": get_families(item[0][0]),
              } for item in zip(groups)]
    return {'liste': liste}


# to get families
def get_families(group_name):
    families_query = Famille.objects.filter(groupe__nom=group_name).values_list('nom', 'pk')
    families = [list(i) for i in families_query]
    liste = []
    for item in range(len(families)):
        temp = {'id':  families[item][1],
                'name': families[item][0],
                # 'subsubmenu': get_sub_families(families[item][0]),
                'url': '#'}
        liste.append(temp)
    return liste


# to get subfamilies
def get_sub_families(family_name):

    subfamilies_queries = SousFamille.objects.filter(famille__nom=family_name).values_list('nom')

    subfamilies = list(itertools.chain(*subfamilies_queries))

    liste = []
    for item in range(len(subfamilies)):
        temp = {'name': subfamilies[item], 'url': '#'}
        liste.append(temp)

    return liste
