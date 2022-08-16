"""
Views da aplicação

"""
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from rest_framework import status
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .sender import get_context
from ..users.permissions import IsOwner
from ..users.models import CustomUser
from ..companies.models import Company
from .models import Monitoring


class MonitoringSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador

    Attributes:
        company (str): Código de referência para a empresa
        user (str): Id (uid) de referência para o usuário

    """

    company = serializers.CharField(source='company.code')
    user = serializers.CharField(source='user.uid', read_only=True)

    class Meta:
        """
        Classe de metadados

        Attributes:
            model: Modelo de banco de dados
            fields: Campos a serem considerados pela API Rest

        """

        model = Monitoring
        fields = ['id', 'company', 'user',
                  'frequency', 'tunnel_min', 'tunnel_max']


class MonitoringViewSet(viewsets.ModelViewSet):
    """
    ViewSet de monitoramento

    Attributes:
        queryset: Query de busca de objetos
        serializer_class: Serializador
        permission_classes: Classe de permissão de acesso à View

    """

    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    permission_classes = [IsOwner]

    def list(self, request, uid):
        """
        Listar monitoramentos de um usuário

        Sobrescrição de listagem dos monitoramentos

        Arguments:
            request: Instância de requisição
            uid: Id do usuário

        Return: (list) Lista de instância de monitoramento

        """

        queryset = Monitoring.objects.filter(user__uid=uid)
        serializer = MonitoringSerializer(queryset, many=True)
        moni = serializer.data

        return Response(moni)

    def create(self, request, uid):
        """
        Criar monitoramento

        Sobescrever função de criação de monitoramento

        Arguments:
            request: Instância de requisição
            uid: Id do usuário

        Return: (Monitoring) Instância de moniotamento

        """
        data = request.data

        user = get_object_or_404(
            CustomUser, uid=uid)
        company = get_object_or_404(
            Company, code=data["company"])

        if Monitoring.objects.filter(user__uid=uid, company__code=data["company"]).exists():
            return Response({"Monitoramento já existente"}, status=status.HTTP_409_CONFLICT)

        serializer = MonitoringSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company, user=user)

        return Response(serializer.data)


class MonitoringDetailsViewSet(viewsets.ModelViewSet):
    """
    ViewSet de detalhamento de monitoramento

    Attributes:
        queryset: Query de busca de objetos
        serializer_class: Serializador
        permission_classes: Classe de permissão de acesso à View

    """
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    permission_classes = [IsOwner]


def email(request, uid, monitoring_id):
    """
    ViewSet do email de monitoramento

    Arguments:
        request: Instância de requisição
        uid: Id do usuário
        monitoring_id: Id do monitoramento

    Return: Template HTML

    """

    template = loader.get_template('email.html')
    context = get_context(uid, monitoring_id)

    return HttpResponse(template.render(context, request))
