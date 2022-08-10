from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path('<uid>', views.UserDetailsViewSet.as_view(
        {'get': 'retrieve'})),
]
