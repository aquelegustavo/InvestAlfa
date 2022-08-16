"""
Views da aplicação

"""
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .permissions import IsOwner


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador

    Attributes: 
        is_active (bool): Usuário está ativo
        is_staff (bool): Usuário é staff
        last_login (Date): Carimbo de data e hora do último login
        date_joined (Date): Carimbo de data e hora em que a conta foi criada
        password (str): Senha do usuário
    """

    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        """
        Classe de metadados

        Attributes:
            model: Modelo de banco de dados
            fields: Campos a serem considerados pela API Rest
            extra_kwargs: Campos adicionais definidos

        """
        model = CustomUser
        fields = ['uid', 'password',
                  'email', 'first_name', 'last_name', 'last_login', 'is_active', 'is_staff', 'date_joined']

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, data):
        """
        Criar usuário

        Sobescrever função de criação de usuário

        Arguments:
            data: Instância dos dados enviados para serialização

        Return: (User) Instância de usuário

        """
        user = super(UsersSerializer, self).create(data)
        user.set_password(data['password'])
        user.username = data["email"]
        user.save()

        return user


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet do Usuário

    Attributes:
        queryset: Query de busca de objetos
        serializer_class: Serializador
        permission_classes: Classe de permissão de acesso à View

    """

    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        """
        Listar usuários

        Sobrescrição de listagem de usuários

        Arguments:
            request: Instância de requisição

        Return: (list) Lista de instância de usuários

        """
        queryset = CustomUser.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        users = serializer.data

        return Response(users)


class UserDetailsViewSet(viewsets.ModelViewSet):
    """
    ViewSet de detalhes do Usuário

    Attributes:
        queryset: Query de busca de objetos
        serializer_class: Serializador
        lookup_field: definição do 'uid' como chave da URL
        permission_classes: Classe de permissão de acesso à View

    """

    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'uid'
    permission_classes = [IsOwner]

    def retrieve(self, request, uid=None):
        """
        Obter detalhes dos usuários

        Sobrescrição da função de detalhamento do usuários

        Arguments:
            request: Instância de requisição
            uid: Id do usuário

        Return: (User) Instância de usuário

        """

        queryset_user = CustomUser.objects.all()
        user = get_object_or_404(queryset_user, uid=uid)

        serializer = UsersSerializer(user)
        return Response(serializer.data)
