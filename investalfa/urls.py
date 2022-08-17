"""
Configurações de URL

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .client import client

urlpatterns = [
    path("", client, name="client"),
    path("signin", client, name="client"),
    path("signup", client, name="client"),
    path('api/quotes/', include('investalfa.apps.quotes.urls')),
    path('api/companies/', include('investalfa.apps.companies.urls')),
    path('api/auth/', include('investalfa.apps.auth.urls')),
    path('api/users/', include('investalfa.apps.users.urls')),
    path('api/users/<uid>/monitoring/',
         include('investalfa.apps.monitoring.urls')),
]
""" URLs da aplicação """
