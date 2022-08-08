from rest_framework import serializers, viewsets
from rest_framework.response import Response

from .models import Quote


class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    code = serializers.CharField(source='parent_company.code')

    class Meta:
        model = Quote
        fields = ['code', 'value', 'timestamp']


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class QuoteDetailsViewSet(viewsets.ModelViewSet):
    def list(self, request):
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
