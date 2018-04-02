from django.shortcuts import render
from rest_framework import (viewsets, permissions)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from servicios.models import (
    Categoria, 
    Servicio, 
    Paquete, 
    Compra,
    CompraDetalle)
from servicios.serializers import (
    CategoriaSerializer, 
    ServicioSerializer, 
    PaqueteSerializer, 
    CompraSerializer,
    CompraDetalleSerializer)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (permissions.AllowAny,)

class ServicioViewSet(viewsets.ModelViewSet):
        queryset = Servicio.objects.all()
        serializer_class = ServicioSerializer
        permission_classes = (permissions.AllowAny,)

class PaqueteViewSet(viewsets.ModelViewSet):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer
    permission_classes = (permissions.AllowAny,)

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = (permissions.AllowAny,)


@permission_classes((permissions.IsAuthenticated,))
class CompraDetalleViewSet(APIView):

    def get(self,request,format=None):
        td = CompraDetalle.objects.filter(compra__cliente__user = request.user)
        serializer = CompraDetalleSerializer(td, many=True)
        return Response(serializer.data)