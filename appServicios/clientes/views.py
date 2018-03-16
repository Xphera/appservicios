from django.contrib.auth.models import User
from django.http import ( HttpResponse, JsonResponse, Http404)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from clientes.models import (Cliente, Ubicacion, MedioDePago)
from clientes.restModels import RegistroCliente
from clientes.serializers import (ClienteSerializer,UbicacionSerializer,UbicacionSerializerApi,MedioDePagoSerializer
    ,RegistroUsuarioSerializer, ValidarEmailUsuarioSerializer,RegistrarInformacionBasicaSerializer)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (viewsets, permissions, mixins, generics, status)






# NIVEL BASICO
"""
@csrf_exempt
def cliente_lista(request):
    if(request.method == 'GET'):
        clientes = Cliente.objects.all()
        clientesSerializer = ClienteSerializer(clientes, many=True)
        return JsonResponse(clientesSerializer.data, safe=False)

    elif(request.method == 'POST'):
        data = JSONParser.parse(request)
        clientesSerializer = ClienteSerializer(data=data)
        if(clientesSerializer.is_valid()):
            clientesSerializer.save()
            return JsonResponse(clientesSerializer.data,status=201)
        return JsonResponse(clientesSerializer.errors,status=404)


@csrf_exempt
def cliente_detalle(request, pk):
    print("Entro")
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        clienteSerializer = ClienteSerializer(cliente)
        return JsonResponse(clienteSerializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        clienteSerializer = ClienteSerializer(cliente, data=data)
        if clienteSerializer.is_valid():
            clienteSerializer.save()
            return JsonResponse(clienteSerializer.data)
        return JsonResponse(clienteSerializer.errors, status=400)

    elif request.method == 'DELETE':
        cliente.delete()
        return HttpResponse(status=204)

"""
#NIVEL 2 -  WRAPPER ANNOTATIONS
"""
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def cliente_lista_wrapper_anotation(request,format=None):

    if request.method == 'GET':
        clientes = Cliente.objects.all()
        clienteSerializer = ClienteSerializer(clientes, many=True)
        return Response(clienteSerializer.data)

    elif request.method == 'POST':
        clienteSerializer = ClienteSerializer(data=request.data)
        if clienteSerializer.is_valid():
            clienteSerializer.save()
            return Response(clienteSerializer.data, status=status.HTTP_201_CREATED)
        return Response(clienteSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def cliente_detalle_wrapper_anotation(request, pk, format=None):
"""
#    Retrieve, update or delete a code snippet.
"""
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        clienteSerializer = ClienteSerializer(cliente)
        return Response(clienteSerializer.data)

    elif request.method == 'PUT':
        clienteSerializer = ClienteSerializer(cliente, data=request.data)
        if clienteSerializer.is_valid():
            clienteSerializer.save()
            return Response(clienteSerializer.data)
        return Response(clienteSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
#nivel 3 -   VIEWS CLASS BASED
"""
@permission_classes((permissions.AllowAny,))
class ClienteClassListView(APIView):
    def get(self, request, format=None):
        clientes = Cliente.objects.all()
        clienteSerializer = ClienteSerializer(clientes, many=True)
        return Response(clienteSerializer.data)
    def post(self, request, format=None):
        clienteSerializer = ClienteSerializer(data=request.data)
        if clienteSerializer.is_valid():
            clienteSerializer.save()
            return Response(clienteSerializer.data, status=status.HTTP_201_CREATED)
        return Response(clienteSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.AllowAny,))
class ClienteDetalleClassView(APIView):
    def get_object(self, pk):
        try:
            return Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cliente = self.get_object(pk)
        clienteSerializer = ClienteSerializer(cliente)
        return Response(clienteSerializer.data)

    def put(self, request, pk, format=None):
        cliente = self.get_object(pk)
        clienteSerializer = ClienteSerializer(cliente, data=request.data)
        if clienteSerializer.is_valid():
            clienteSerializer.save()
            return Response(clienteSerializer.data)
        return Response(clienteSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cliente = self.get_object(pk)
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


# con MIXINS
"""
class ClienteMiximsList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClienteMiximDetalle(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""

# con Generics
"""
    class ClienteGenericsList(generics.ListCreateAPIView):
        queryset = Cliente.objects.all()
        serializer_class = ClienteSerializer
    
    
    class ClienteGenericsDetalle(generics.RetrieveUpdateDestroyAPIView):
        queryset = Cliente.objects.all()
        serializer_class = ClienteSerializer
    
    
    
    class RegistroClienteDetalle(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
        queryset = User.objects.all()
        serializer_class = RegistroUsuarioSerializer
    
        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)
    
        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)


"""
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
class ModificarInformacionAdicional(APIView):
    def put(self,request,format=None):
        data = request.data
        email_usuario = request.user.email
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

@permission_classes((permissions.IsAuthenticated,))
class ClienteUbicaciones(APIView):
    
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
                return Response(ubicacionesSerializer.data)
            except Exception as e:
                return Response({"estado": "error", "msj": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(ubicacionesSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,format=None):
        
        data = request.data
        cliente = Cliente.objects.get(user_id=request.user.id)
        data["cliente"] = cliente.id
        ubicacion = Ubicacion.objects.get(pk=pk)

        if (cliente.id == ubicacion.cliente_id):
            ubicacionesSerializer = UbicacionSerializerApi(ubicacion,data=data)                
            if ubicacionesSerializer.is_valid():
                try:
                    ubicacionesSerializer.save()
                    return Response({"estado": "ok"}, status=status.HTTP_202_ACCEPTED)
                except Exception as e:
                    return Response({"estado": "error", "msj": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(ubicacionesSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({"estado": "error", "msj": "Ubicación No pertenece a usuario"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request,pk,format=None):
        
            try:          
                ubicacion = Ubicacion.objects.get(pk=pk)
                cliente = Cliente.objects.get(user_id=request.user.id)
                if (cliente.id == ubicacion.cliente_id):                
                    ubicacion.delete()
                    return Response({"estado": "ok"}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"estado": "error", "msj": "Ubicación No pertenece a usuario"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)             
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