from django.http import HttpResponse
from .data import data


def index(request):
    data()
    return HttpResponse("O mulher, salva ai no db! #mulherLibera")
