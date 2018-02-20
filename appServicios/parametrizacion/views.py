from django.shortcuts import render
from rest_framework import (viewsets, permissions)
from parametrizacion.models import (Departamento, Municipio)
from parametrizacion.serializers import (DepartamentoSerializer, MunicipioSerializer)

# Create your views here.


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = (permissions.AllowAny,)

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = (permissions.AllowAny,)