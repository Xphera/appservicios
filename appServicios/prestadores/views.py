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
from .logica.logicaPrestador import LogicaPrestador

from django.contrib.gis.geos import (GEOSGeometry)
from prestadores.permissions import EsPrestador
from utils.Utils.usuario import Usuario


# Create your views here. 

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class CambiarPassword(APIView):
   
    def put(self, request,format=None):

        output = Usuario().cambioContrenia(request)
        if(output["estado"]):
            return Response({"estado":"ok","token": output["token"]}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST)  

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class CambiarUsuario(APIView):
   
    def post(self, request,format=None):
        output = Usuario().cambioUsuario(request)
        if(output["estado"]):
            return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST)
    def put(self, request,format=None):

        output = Usuario().cambioUsuarioValidarCodigo(request)
        if(output["estado"]):
            return Response({"estado":"ok","token": output["token"]}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class RestablecerPassword(APIView):
   
    def post(self, request,format=None):
        output = Usuario().restablecerPassword(request)
        if(output["estado"]):
            return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST)

    def put(self, request,format=None):

        output = Usuario().restablecerPasswordValidaCodigo(request)
        if(output["estado"]):
            return Response({"estado":"ok","token": output["token"]}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST)

        
@permission_classes((EsPrestador,))
class PrestadorViewSet(APIView):
    
    def get(self, request,format=None):
        params = self.request.query_params
        if(params.get("latitud",None) and params.get("longitud",None)):   
            logicaPrestador = LogicaPrestador()         
            return Response(
            logicaPrestador.geolocalizarPrestadorServicio(
                params.get("longitud",None),
                params.get("latitud",None),
                params.get("servicio",None)
                )    
            )
        elif(params.get("servicio",None)):   
            logicaPrestador = LogicaPrestador()         
            return Response( 
            logicaPrestador.PrestadorPorServicio(
                params.get("servicio",None)
                )    
            )  
        elif (params.get("userId",None)):
            logicaPrestador = LogicaPrestador()
            return Response(logicaPrestador.customSerializer(Prestador.objects.get(user = request.user),None), status=status.HTTP_202_ACCEPTED)          
        else:
            # q=Prestador.objects.all()
            # p= PrestadorSerializer(q,many=True)
            return Response({}, status=status.HTTP_202_ACCEPTED)
        
    def put(self,request,id,format=None):
        prestador = Prestador.objects.get(pk=id)
        serializer = PrestadorSerializer(prestador,data=request.data) 
        if(serializer.is_valid()):
            serializer.save()
            return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
        else:
             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)   
        

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
class SesionFinalizadaViewSet(APIView):    
    def get(self, request,format=None):
        sesiones = Sesion()   
        serializer = CompraDetalleSesioneSerializer(sesiones.finalizada(request.user.id),many=True)
        return Response(serializer.data)

@permission_classes((permissions.IsAuthenticated,EsPrestador,))
class SesionIniciadaViewSet(APIView):
    
    def get(self, request,format=None):
        sesiones = Sesion()   
        serializer = CompraDetalleSesioneSerializer(sesiones.iniciada(request.user.id),many=True)
        return Response(serializer.data)
