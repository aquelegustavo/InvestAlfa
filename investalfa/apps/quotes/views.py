"""
Views da aplicação

"""
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Quote


class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador

    Attributes: 
        code (str): Código de referência para a empresa
    """

    code = serializers.CharField(source='parent_company.code')

    class Meta:
        """
        Classe de metadados

        Attributes:
            model: Modelo de banco de dados
            fields: Campos a serem considerados pela API Rest

        """

        model = Quote
        fields = ['code', 'value', 'timestamp']


class QuoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet das cotações

    Attributes:
        queryset: Query de busca de objetos
        serializer_class: Serializador
        permission_classes: Classe de permissão de acesso à View

    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [AllowAny]


class QuoteDetailsViewSet(viewsets.ModelViewSet):
    """
    ViewSet de detalhes das cotações

    Attributes:
        permission_classes: Classe de permissão de acesso à View

    """
    permission_classes = [AllowAny]

    def list(self, request):
        """
        Listar Cotações

        Sobrescrição de listagem de cotações

        Arguments:
            request: Instância de requisição

        Return: (list) Lista de instância de cotações

        """

        queryset = Quote.objects.all()
        serializer = QuoteSerializer(queryset, many=True)
        data = serializer.data

        response = {}

        for item in data:
            if not item["code"] in response:
                response[item["code"]] = []

            response[item["code"]].append({
                "value": item["value"],
                "timestamp": item["timestamp"],
            })

        return Response(response)
