from django.contrib.auth.models import User
from django.http import ( HttpResponse, JsonResponse, Http404)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from clientes.models import (Cliente, Ubicacion, MedioDePago)
from clientes.restModels import RegistroCliente
from clientes.serializers import (
    ClienteSerializer,
    UbicacionSerializer,
    UbicacionSerializerApi,
    MedioDePagoSerializer,
    RegistroUsuarioSerializer, 
    ValidarEmailUsuarioSerializer,
    RegistrarInformacionBasicaSerializer,
    CambiarUsuarioSerializer,
    CambiarUsuarioValidarCodigoSerializer)

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (viewsets, permissions, mixins, generics, status)


from utils.Utils.usuario import Usuario


from clientes.permissions import EsDueño


@permission_classes((permissions.AllowAny,))
class RegistroClienteList(APIView):
    def post(self, request, format=None):
        registroUsuarioSerializer = RegistroUsuarioSerializer(data=request.data)
        if registroUsuarioSerializer.is_valid():
            registroUsuarioSerializer.save()
            return Response(registroUsuarioSerializer.data, status=status.HTTP_201_CREATED)
        return Response(registroUsuarioSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



@permission_classes((permissions.AllowAny,))
class ValidarEmailCode(APIView):
    def post(self, request,format=None):

        veus =  ValidarEmailUsuarioSerializer(data=request.data)

        if veus.is_valid():
            try:
                veus.save()
                return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
            except(e):
                return Response({"estado": "error","msj":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(veus.errors, status= status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,))
class CambiarPassword(APIView):
   
    def put(self, request,format=None):

        output = Usuario().cambioContrenia(request)
        if(output["estado"]):
            return Response({"estado":"ok","token": output["token"]}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST) 
     


@permission_classes((permissions.IsAuthenticated,))
class CambiarUsuarioValidarCodigo(APIView):
    def put(self, request,format=None):
        output = Usuario().cambioUsuarioValidarCodigo(request)
        if(output["estado"]):
            return Response({"estado":"ok","token": output["token"]}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticated,))
class CambiarUsuario(APIView):
   
    def post(self, request,format=None):
        output = Usuario().cambioUsuario(request)
        if(output["estado"]):
            return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
        else:    
            return Response(output["error"], status= status.HTTP_400_BAD_REQUEST)        


@permission_classes((permissions.IsAuthenticated,))
class Informacion(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,format=None):
        cliente = Cliente.objects.get(user_id=request.user.id)
        clienteSerializer = RegistrarInformacionBasicaSerializer(cliente)
        return Response(clienteSerializer.data,status= status.HTTP_200_OK)

    def put(self,request,format=None):        
        data = request.data
        data["email"] = request.user.email
        
        registrarSerializer = RegistrarInformacionBasicaSerializer(data=data)
        
        if registrarSerializer.is_valid():
            try:
                registrarSerializer.save()
                return Response({"estado": "ok"}, status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                return Response({"estado": "error", "msj": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(registrarSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def has_permission(self, request, view):
        '''
        
        value = request.data('some_integer_field', None)
        user = request.user

        if view.action == 'create':
            if user.name == 'David' and value > 5:
                return False
        '''

        return True

class ClienteUbicaciones(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self,request,format=None):
        ubicaciones = Ubicacion.objects.filter(cliente__user = request.user)
        ubicacionesSerializer = UbicacionSerializerApi(ubicaciones, many=True)
        return Response(ubicacionesSerializer.data)

    def post(self,request,format=None):
        data = request.data
        cliente = Cliente.objects.get(user_id=request.user.id)
        data["cliente"] =  cliente.id
        ubicacionesSerializer = UbicacionSerializerApi(data=request.data)
        if ubicacionesSerializer.is_valid():
            try:
                ubicacionesSerializer.save()
                return Response({"estado": "ok"}, status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                return Response({"estado": "error", "msj": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(ubicacionesSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteUbicacion(APIView):

    permission_classes= (EsDueño,)

    def get(self,request,id,format=None):
        if(Ubicacion.objects.filter(pk=id).count()>0):
            ubicacion = Ubicacion.objects.get(id=id)
            self.check_object_permissions(self.request,ubicacion)
            ubicacionesSerializer = UbicacionSerializerApi(ubicacion)
            return Response(ubicacionesSerializer.data)
        else:
            return Response("La Ubicacion no existe", status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id,format=None):
        if(Ubicacion.objects.filter(pk=id).count()>0):
            data = request.data            
            ubicacion = Ubicacion.objects.get(pk=id)
            data['cliente'] = ubicacion.cliente.id
            self.check_object_permissions(self.request,ubicacion)
            ubicacionesSerializer = UbicacionSerializerApi(ubicacion, data=request.data)
            if(ubicacionesSerializer.is_valid()):
                ubicacionesSerializer.save()
                return Response(ubicacionesSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(ubicacionesSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("La Ubicacion no existe", status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id,format=None):
        
            try:
                ubicacion = Ubicacion.objects.get(pk=id)
                self.check_object_permissions(self.request,ubicacion)
                ubicacion.delete()
                return Response({"estado": "ok"}, status=status.HTTP_202_ACCEPTED)          
            except Exception as e:
                return Response({"estado": "error", "msj": str(e)}, status=status.HTTP_400_BAD_REQUEST)
             


# VIEWS SETS PARA API NAVEGABLE

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
    permission_classes = (permissions.IsAuthenticated,)

class MediodepagoViewSet(viewsets.ModelViewSet):
    queryset = MedioDePago.objects.all()
    serializer_class = MedioDePagoSerializer
    permission_classes = (permissions.IsAuthenticated,)