from django.urls import path

from . import views

urlpatterns = [
    path('', views.MonitoringViewSet.as_view(
        {'get': 'list',
         'post': 'create'},
    )),
    path('/<pk>/', views.MonitoringDetailsViewSet.as_view(
        {'delete': 'destroy',
         'put': 'partial_update'},
    )),
    path('/<monitoring_id>/emails', views.email),

]
