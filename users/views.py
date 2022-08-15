from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.models import CustomUser
from .permissions import IsOwner


class UsersSerializer(serializers.HyperlinkedModelSerializer):

    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['uid', 'password',
                  'email', 'first_name', 'last_name', 'last_login', 'is_active', 'is_staff', 'date_joined']

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, data):
        user = super(UsersSerializer, self).create(data)
        user.set_password(data['password'])
        user.username = data["email"]
        user.save()

        return user


class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        users = serializer.data

        return Response(users)


class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'uid'
    permission_classes = [IsOwner]

    def retrieve(self, request, uid=None):

        queryset_user = CustomUser.objects.all()
        user = get_object_or_404(queryset_user, uid=uid)

        serializer = UsersSerializer(user)
        return Response(serializer.data)
