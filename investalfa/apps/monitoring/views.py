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
    company = serializers.CharField(source='company.code')
    user = serializers.CharField(source='user.uid', read_only=True)

    class Meta:
        model = Monitoring
        fields = ['id', 'company', 'user',
                  'frequency', 'tunnel_min', 'tunnel_max']


class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    permission_classes = [IsOwner]

    def list(self, request, uid):
        queryset = Monitoring.objects.filter(user__uid=uid)
        serializer = MonitoringSerializer(queryset, many=True)
        moni = serializer.data

        return Response(moni)

    def create(self, request, uid):
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
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    permission_classes = [IsOwner]


def email(request, uid, monitoring_id):

    template = loader.get_template('email.html')
    context = get_context(uid, monitoring_id)

    return HttpResponse(template.render(context, request))
