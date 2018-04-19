from django.shortcuts import render
from rest_framework import (viewsets, permissions,status)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes

from prestadores.models import Prestador,Disponibilidad
from prestadores.serializers import (PrestadorSerializer,programacionSegunSesionSerializer,disponibilidadMesSerializer)
from .logica.disponibilidad import Disponibilidad

# Create your views here.

class PrestadorViewSet(viewsets.ModelViewSet):
    queryset = Prestador.objects.all()
    serializer_class = PrestadorSerializer
    permission_classes = (permissions.AllowAny,)



@permission_classes((permissions.AllowAny,))
class DisponibilidadViewSet(APIView):
    
    def get(self, request,format=None):
        disponibilidad = Disponibilidad()
        return Response(disponibilidad.obtener(1))

    def post(self, request,format=None):
        disponibilidad = Disponibilidad()
        guardar = disponibilidad.guardar(request)
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
class disponibilidadMesSegunSesion(APIView):
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
