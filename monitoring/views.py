from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response

from users.models import CustomUser
from companies.models import Company

from .models import Monitoring


class MonitoringSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.CharField(source='company.code')
    user = serializers.CharField(source='user.uid')

    class Meta:
        model = Monitoring
        fields = ['company', 'user', 'frequency', 'tunnel_min', 'tunnel_max']


class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    def list(self, request, uid):
        queryset = get_object_or_404(Monitoring, user=uid)

        serializer = MonitoringSerializer(queryset, many=True)
        monitoring = serializer.data

        return Response(monitoring)

    def create(self, request, uid):
        data = request.data

        user = get_object_or_404(
            CustomUser, uid=data["user"])
        company = get_object_or_404(
            Company, code=data["company"])

        serializer = MonitoringSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save(company=company, user=user)

        return Response("ok")
