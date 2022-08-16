"""
Configurações de URLs

"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.CompanyViewSet.as_view({'get': 'list'})),
    path('<str:code>/',
         views.CompanyDetailsViewSet.as_view({'get': 'retrieve'})),
]
""" URLs da aplicação """
