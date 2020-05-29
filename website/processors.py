from django.shortcuts import render

from website.models import Groupe


def my_context_processor(request):
    # groups = [group.nom for group in Groupe.objects.all()]
    groups = Groupe.objects.all()
    print(groups)
    return render(request, "_navbar.html", {'groups': groups})