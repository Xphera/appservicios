import json
from django.shortcuts import render
from rest_framework import (viewsets, permissions,status)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import permission_classes

from prestadores.models import Prestador,Disponibilidad
from prestadores.serializers import (
    PrestadorSerializer,
    programacionSegunSesionSerializer,
    disponibilidadMesSerializer,
    zonaSerializer)

from servicios.serializers import (
    CompraDetalleSesioneSerializer,
)


from .logica.disponibilidad import Disponibilidad
from .logica.sesion import Sesion
from django.contrib.gis.geos import (GEOSGeometry)

from prestadores.permissions import EsPrestador

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
        elif (params.get("id",None)):
            queryset = Prestador.objects.filter(user_id=params.get("id",None))
            return queryset  
        


# @permission_classes((permissions.AllowAny,))
# class PrestadorViewSet(APIView):
    
#     def get(self, request,format=None):
#         prestador = Prestador.objects.get(user_id = 1) 
#         serializer = PrestadorSerializer(prestador)
#         return Response(serializer.data)


#     def post(self, request,format=None):
#         disponibilidad = Disponibilidad()
  
#         guardar = disponibilidad.guardar(request.data["disponibilidad"])
#         if(guardar==True):      
#             return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(guardar, status= status.HTTP_400_BAD_REQUEST)  


@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class DisponibilidadViewSet(APIView):
    
    def get(self, request,format=None):
        disponibilidad = Disponibilidad()
        return Response(disponibilidad.obtener(request.user.id))

    def post(self, request,format=None):
        disponibilidad = Disponibilidad()
        data = request.data
        data["usuarioId"] = request.user.id
        guardar = disponibilidad.guardar(data)
        if(guardar==True):      
            return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(guardar, status= status.HTTP_400_BAD_REQUEST)  

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
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

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class zonaViewSet(APIView):
    def post(self,request,format=None):
        data=request.data
        geodata = json.loads(data["geodata"])
        data["zonaId"] = geodata["id"]
        data["usuarioId"] = request.user.id
        serializer = zonaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"estado":"ok"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):

        qs = Prestador.objects.get( 
            user_id = request.user.id
        ) 
        if qs:
            serializer = zonaSerializer(qs.zona)
            return Response(serializer.data)
        else:
            return Response({})         

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class SesionPorIniciarViewSet(APIView):
    def get(self, request,format=None):
        sesiones = Sesion()   
        serializer = CompraDetalleSesioneSerializer(sesiones.porIniciar(request.user.id),many=True)
        return Response(serializer.data)

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class SesionProximaViewSet(APIView):
    
    def get(self, request,format=None):
        sesiones = Sesion()   
        serializer = CompraDetalleSesioneSerializer(sesiones.proximas(request.user.id),many=True)
        return Response(serializer.data)

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class SesionFinalizadaViewSet(ListAPIView):    
    def get(self, request,format=None):
        sesiones = Sesion()   
        serializer = CompraDetalleSesioneSerializer(sesiones.finalizada(request.user.id),many=True)
        return Response(serializer.data)

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class SesionIniciadaViewSet(ListAPIView):
    
    def get(self, request,format=None):
        sesiones = Sesion()   
        serializer = CompraDetalleSesioneSerializer(sesiones.iniciada(request.user.id),many=True)
        return Response(serializer.data)
