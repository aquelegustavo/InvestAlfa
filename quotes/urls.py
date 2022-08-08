from django.urls import path

from . import views

urlpatterns = [
    path('', views.QuoteViewSet.as_view({'get': 'list'})),
    path('/charts',
         views.QuoteDetailsViewSet.as_view({'get': 'list'})),
]
