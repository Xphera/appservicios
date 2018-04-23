from django.shortcuts import render
from rest_framework import (viewsets, permissions,status)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
import dateparser
from datetime import datetime

from parametrizacion.models import (EstadoCompraDetalleSesion)

# Create your views here.
from servicios.models import (
    Categoria, 
    Servicio, 
    Paquete, 
    Compra,
    CompraDetalle,
    CompraDetalleSesion)
from servicios.serializers import (
    CategoriaSerializer, 
    ServicioSerializer, 
    PaqueteSerializer, 
    CompraSerializer,
    CompraDetalleSerializer,
    CompraDetalleSesioneSerializer,
    CalificarSesionSerializer,
    ProgramarSesionSerializer)

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
class CalificarSesionViewSet(APIView):

    def get(self,request,format=None):
        # ,compraDetalle__estado_id=1
        qs = CompraDetalleSesion.objects.filter(compraDetalle__compra__cliente__user = request.user,estado=3,calificacion=0).order_by("fechaInicio").first()
        if qs:
            serializer = CompraDetalleSesioneSerializer(qs,many=False)
            return Response(serializer.data)
        else:
            return Response({})

    def post(self,request,format=None):
        data = request.data
        data['userId'] = request.user.id
        serializer = CalificarSesionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"estado":"ok"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,))
class ProximaSesionViewSet(APIView):
 
    def get(self,request,format=None):
        qs = CompraDetalleSesion.objects.filter(compraDetalle__compra__cliente__user = request.user,estado=2,compraDetalle__estado_id=1,calificacion=0).order_by("fechaInicio").first()               
        if qs:
            serializer = CompraDetalleSesioneSerializer(qs,many=False)
            return Response(serializer.data)
        else:
            return Response({}) 

@permission_classes((permissions.IsAuthenticated,))
class PaqueteActivoViewSet(APIView):
    
    def get(self,request,format=None):
        #todo: contenplar la posiblidad que haya mas de un paquete activo
        try:
            qs = CompraDetalle.objects.get(compra__cliente__user = request.user,estado=1)
            
            serializer = CompraDetalleSerializer(qs)
            return Response(serializer.data)
        except Exception as e:
             print (e)
             return Response({})

@permission_classes((permissions.IsAuthenticated,))
class ProgramarSesionViewSet(APIView):

     def post(self,request,format=None):
        
        fi = dateparser.parse(request.data["fecha"]) 
        data = request.data
        data["fechaInicio"]=  datetime(fi.year,fi.month,fi.day,fi.hour)
        data["userId"]= request.user.id
        serializer= ProgramarSesionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"estado":"ok"})
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)