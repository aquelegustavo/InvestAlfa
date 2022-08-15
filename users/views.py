from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from users.models import CustomUser
from .permissions import IsOwner


class UsersSerializer(serializers.HyperlinkedModelSerializer):

    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['uid', 'password',
                  'email', 'first_name', 'last_name', 'last_login', 'is_active', 'is_staff', 'date_joined']

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class CreateUserPermission(permissions.BasePermission):
    """
    Liberação para criação de usuários
    """

    def has_permission(self, request, view):
        return request.method == "POST"


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | CreateUserPermission]

    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        users = serializer.data

        for user in users:
            user.pop("password")

        return Response(users)

    def create(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=request.data["email"])

        return Response(serializer.data)


class UserDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    def retrieve(self, request, uid=None):

        queryset_user = CustomUser.objects.all()
        user = get_object_or_404(queryset_user, uid=uid)

        user.pop("password")

        serializer = UsersSerializer(user)
        return Response(serializer.data)
