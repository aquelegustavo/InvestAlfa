from django.urls import path

from . import views

urlpatterns = [
    path('', views.CompanyViewSet.as_view({'get': 'list'})),
]
