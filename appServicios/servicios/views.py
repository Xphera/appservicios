from django.shortcuts import render
from rest_framework import (viewsets, permissions)
# Create your views here.
from servicios.models import (Categoria, Servicio, Paquete, Compra)
from servicios.serializers import (CategoriaSerializer, ServicioSerializer, PaqueteSerializer, CompraSerializer)

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