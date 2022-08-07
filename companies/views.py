from django.http import JsonResponse
from django.core import serializers
from companies.models import Company


def get_companies(request):
    data = serializers.serialize("json", Company.objects.all())
    return JsonResponse(data, safe=False)
