import json
from django.shortcuts import render
from rest_framework import (viewsets, permissions,status)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes

from prestadores.models import Prestador,Disponibilidad
from prestadores.serializers import (
    PrestadorSerializer,
    programacionSegunSesionSerializer,
    disponibilidadMesSerializer,
    zonaSerializer)
from .logica.disponibilidad import Disponibilidad
from django.contrib.gis.geos import (GEOSGeometry)

# Create your views here.

class PrestadorViewSet(viewsets.ModelViewSet):
   
    
    serializer_class = PrestadorSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):  
        output = []      
        params = self.request.query_params
        if(params.get("latitud",None) and params.get("longitud",None)):
            pnt = GEOSGeometry('POINT('+str(params.get("longitud",None))+' '+str(params.get("latitud",None))+')')
            queryset = Prestador.objects.filter(zona__zona__intersects=(pnt),servicios__id = params.get("servicio",None))
            # return queryset
            # refinado busqueda de puntos en polygono
            for q in queryset:
                if(q.zona.zona.intersects(pnt)):
                    output.append(q)
            return output       

@permission_classes((permissions.AllowAny,))
class DisponibilidadViewSet(APIView):
    
    def get(self, request,format=None):
        disponibilidad = Disponibilidad()
        return Response(disponibilidad.obtener(1))

    def post(self, request,format=None):
        disponibilidad = Disponibilidad()
  
        guardar = disponibilidad.guardar(request.data["disponibilidad"])
        if(guardar==True):      
            return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(guardar, status= status.HTTP_400_BAD_REQUEST)  

@permission_classes((permissions.IsAuthenticated,))
class programacionSegunSesionViewSet(APIView):
    
     def post(self, request,format=None):
        data = request.data
        data["usuarioId"] = request.user.id
        serializer = programacionSegunSesionSerializer(data=request.data)
        if serializer.is_valid():
            disponibilidad = Disponibilidad()
            output = disponibilidad.programacionSegunSesion(request.data)
            return Response(output)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticated,))
class disponibilidadMesSegunSesionViewSet(APIView):
    def post(self, request,format=None):
        data= request.data
        data["usuarioId"]=request.user.id
        serializer = disponibilidadMesSerializer(data=data)
        if serializer.is_valid():
            disponibilidad = Disponibilidad()
            output =  disponibilidad.disponibilidadMesSegunSesion(request.data["año"],request.data["mes"],request.data["sesionId"])
            return Response(output)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,))
class zonaViewSet(APIView):
    def put(self,request,pk,format=None):
        data=request.data
        geodata = json.loads(data["geodata"])
        # g= GEOSGeometry(str(geodata["geometry"]))
        data["zonaId"] = geodata["id"]
        data["usuarioId"] = request.user.id
        # print(data["zona"])
        serializer = zonaSerializer(pk,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"estado":"ok"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
