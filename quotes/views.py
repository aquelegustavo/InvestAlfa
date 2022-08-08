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
