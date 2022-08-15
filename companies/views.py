from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from companies.models import Company
from quotes.models import Quote


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'code', 'last_quote', 'min_quote', 'max_quote']


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, code=None):

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
