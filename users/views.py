from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from users.models import CustomUser


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

    def create(self, data):
        user = CustomUser.objects.create(
            username=data['email'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        user.set_password(data['password'])
        user.save()

        return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        users = serializer.data

        for user in users:
            user.pop("password")

        return Response(users)


class UserDetailsViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, uid=None):

        queryset_user = CustomUser.objects.all()
        user = get_object_or_404(queryset_user, uid=uid)

        serializer = UsersSerializer(user)
        return Response(serializer.data)
