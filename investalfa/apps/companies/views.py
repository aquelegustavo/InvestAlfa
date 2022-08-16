"""
Views da aplicação

"""
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..companies.models import Company
from ..quotes.models import Quote


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador

    """

    class Meta:
        """
        Classe de metadados

        Attributes:
            model: Modelo de banco de dados
            fields: Campos a serem considerados pela API Rest

        """
        model = Company
        fields = ['name', 'code', 'last_quote', 'min_quote', 'max_quote']


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet das empresas

    Attributes:
        queryset: Query de busca de objetos
        serializer_class: Serializador
        permission_classes: Classe de permissão de acesso à View

    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]


class CompanyDetailsViewSet(viewsets.ModelViewSet):
    """
    ViewSet de detalhamento das empresas

    Attributes:
        permission_classes: Classe de permissão de acesso à View

    """

    permission_classes = [AllowAny]

    def retrieve(self, request, code=None):
        """
        Obter detalhes das empresas

        Sobrescrição da função de detalhamento da empresa

        Arguments:
            request: Instância de requisição
            code: Código de referência para empresa

        Return: (Company) Instância da empresa

        """

        queryset_company = Company.objects.all()
        company = get_object_or_404(queryset_company, code=code)

        quotes = Quote.objects.filter(parent_company=company)

        data = []

        for q in quotes:
            data.append({
                "value": q.value,
                "timestamp": q.timestamp
            })

        serializer = CompanySerializer(company)

        response = serializer.data
        response["data"] = data
        return Response(response)
