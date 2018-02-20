from django.shortcuts import render
from rest_framework import (viewsets, permissions)


from prestadores.models import Prestador
from prestadores.serializers import PrestadorSerializer
# Create your views here.

class PrestadorViewSet(viewsets.ModelViewSet):
    queryset = Prestador.objects.all()
    serializer_class = PrestadorSerializer
    permission_classes = (permissions.AllowAny,)