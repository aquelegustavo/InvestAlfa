from django.urls import path

from . import views

urlpatterns = [
    path('', views.MonitoringViewSet.as_view(
        {'get': 'list',
         'post': 'create'},
    )),
]
