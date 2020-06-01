from website.models import Groupe, Famille

""" Dynamic menus and submenus from DB"""


# to get parent menu
def get_menus():
    group_query = Groupe.objects.all().values_list('nom')  # Groupe
    groups = [list(i) for i in group_query]

    liste = [{"name": item[0][0], 'url': '#',  # retrieve query to array of dictionnaries
              'validators': ["menu_generator.validators.is_authenticated"],
              "submenu": get_families(item[0][0])
              } for item in zip(groups)]

    return liste


# to get submenu
def get_families(group_name):
    # [{"name": "1","url": "/1",},{"name": "2","url": "/2",},]
    print(group_name)
    famillies_query = Famille.objects.filter(groupe__nom=group_name).values_list('nom')
    print(famillies_query)
    famillies = [list(i) for i in famillies_query]
    liste = []
    for item in range(len(famillies)):
        temp = {'name': famillies[item][0], 'url': '#'}
        liste.append(temp)
    return liste


MENUS = {
    'NAV_MENU_TOP': [
        {
            "name": "Logo",
            "url": "/",
            "validators": ["menu_generator.validators.is_authenticated"],
        },
        {
            "name": "Deconnexion",
            "url": "/logout",
            "validators": ["menu_generator.validators.is_authenticated"],
        },
    ],
    'NAV_MENU_LEFT': get_menus()
}
