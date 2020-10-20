import itertools
from django.db.models import Q
from website.models import Groupe, Famille, SousFamille, Article
from django.db.models import Count

""" Dynamic menus and submenus from DB"""


def groups_to_exclude():
    """
    if less than 10 articles
    """
    articles_by_group = Groupe.objects.all().annotate(nbre=Count('article_by_group'))
    result = []
    for key, value in enumerate(articles_by_group):
        if value.nbre < 10:
            result.append(articles_by_group[key].nom)
    return result


def get_menus(request):
    """
    groups
    """
    group_query = Groupe.objects.all().exclude(
        Q(nom__in=groups_to_exclude())
    ).order_by('ordre').values_list('nom', 'pk')
    groups = [list(i) for i in group_query]
    liste = [{"id": item[0][1],
              "name": item[0][0], 'url': '#',  # retrieve query to array of dictionnaries
              'validators': ["menu_generator.validators.is_authenticated"],
              "submenu": get_families(item[0][0]),
              } for item in zip(groups)]
    return {'liste': liste}


def families_to_exclude():
    """
    if less than 10 articles
    """
    articles_by_family = Famille.objects.all().annotate(nbre=Count('article_by_familly'))
    result = []
    for key, value in enumerate(articles_by_family):
        if value.nbre < 10:
            result.append(articles_by_family[key].nom)
    return result


def get_families(group_name):
    """
    sub families
    """
    group = Groupe.objects.get(nom=group_name).id
    families = Famille.objects.filter(groupe__id=group)
    liste = []
    for fam in families:
        rst = Article.objects.filter(Q(groupe__pk=group) & Q(famille__pk=fam.pk)).count()
        if rst > 1:
            families_query = Famille.objects.filter(id=fam.pk).exclude(
                Q(nom__in=families_to_exclude())
            ).values_list('nom', 'pk')
            families = [list(i) for i in families_query]

            for item in range(len(families)):
                temp = {'id': families[item][1],
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
