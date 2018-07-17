import json
from django.shortcuts import render
from rest_framework import (viewsets, permissions,status)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
import dateparser
from datetime import datetime
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q

from parametrizacion.models import (EstadoCompraDetalleSesion)

from  servicios.logica.paquete import Paquete as PaqueteLogica


from servicios.models import (
    Categoria, 
    Servicio, 
    Paquete, 
    Compra,
    CompraDetalle,
    CompraDetalleSesion,
    Zona )
from servicios.serializers import (
    CategoriaSerializer, 
    ServicioSerializer, 
    PaqueteSerializer, 
    CompraSerializer,
    CompraDetalleSerializer,
    CompraDetalleSesioneSerializer,
    CalificarSesionSerializer,
    ProgramarSesionSerializer,
    ZonaSerializer,
    IniciarSesionSerializer,
    FinalizarSesionSerializer,
    CancelarSesionSerializer,
    CancelarPaqueteSerializer,
    RenovarPaqueteSerializer)

from prestadores.permissions import EsPrestador    

from django.core.serializers import serialize

# Create your views here.

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
        qs = CompraDetalleSesion.objects.filter(
            Q(estado_id=2)  | Q(estado_id=4),
            compraDetalle__compra__cliente__user = request.user,
            # estado=2,
            compraDetalle__estado_id=1,
            calificacion=0
            ).order_by("fechaInicio").first()               
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class ZonaSesionViewSet(APIView):
    def get(self,request,format=None):
        qs = Zona.objects.all()
        if qs:
            serializer = ZonaSerializer(qs,many=True)
            return Response(serializer.data)
        else:
            return Response({})

    def post(self,request,format=None):
        data=request.data
        data["zona"] = GEOSGeometry(str(json.loads(data["zona"])["geometry"]))
        serializer = ZonaSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"estado":"ok"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,format=None):
        data=request.data
        data["zona"] = GEOSGeometry(str(json.loads(data["zona"])["geometry"]))
        serializer = ZonaSerializer(pk,data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"estado":"ok"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)    

    def delete(self,request,pk,format=None):
        data=request.data
        z=Zona.objects.get(pk=pk)
        z.delete()
        return Response({"estado":"ok"}, status=status.HTTP_200_OK)
        # if(serializer.is_valid()):
        #     serializer.save()
        #     return Response({"estado":"ok"}, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class IniciarSesionViewSet(APIView):
    
    def post(self, request,format=None):        
        data = request.data
        data["userId"] = request.user.id      
        serializer = IniciarSesionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)  

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class FinalizarSesionViewSet(APIView):
    
    def post(self, request,format=None):        
        data = request.data
        data["userId"] = request.user.id

        serializer = FinalizarSesionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST) 

@permission_classes((permissions.IsAuthenticated,))
class CancelarSesionViewSet(APIView):
    
    def post(self, request,format=None):        
        data = request.data
        data["userId"] = request.user.id

        serializer = CancelarSesionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,))
class CancelarPaqueteViewSet(APIView):
    def post(self, request,format=None):
        data = request.data
        data["userId"] = request.user.id
        serializer = CancelarPaqueteSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'ok'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,))
class RenovarPaqueteViewSet(APIView):
    def post(self, request,format=None):
        data = request.data
        data["userId"] = request.user.id
        serializer = RenovarPaqueteSerializer(data=data)
        if(serializer.is_valid()):
            p = PaqueteLogica()     
            renovar = p.renovarPaquete(data["userId"],data["compraDetalleId"])
            return Response(renovar, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

