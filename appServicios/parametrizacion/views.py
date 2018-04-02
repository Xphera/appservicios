from django.shortcuts import render
from rest_framework import (viewsets, permissions)
from parametrizacion.models import (Departamento, Municipio,Sexo)
from parametrizacion.serializers import (DepartamentoSerializer, MunicipioSerializer, SexoSerializer)

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = (permissions.AllowAny,)

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = (permissions.AllowAny,)

@permission_classes((permissions.AllowAny,))
class SexoViewSet(APIView):
    def get(self,request,format=None):
        sexo = Sexo.objects.all()
        sexoSerializer = SexoSerializer(sexo,many=True)
        return Response(sexoSerializer.data)