from django.shortcuts import render



from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from clientes.models import (Cliente, Ubicacion, MedioDePago)
from django.contrib.auth.models import User
from clientes.serializers import (ClienteSerializer,UbicacionSerializer,MedioDePagoSerializer ,RegistroUsuarioSerializer)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework import (viewsets, permissions)
from rest_framework.response import Response

from clientes.restModels import RegistroCliente

from rest_framework.views import APIView
from django.http import Http404


from rest_framework import mixins
from rest_framework import generics

# NIVEL BASICO
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

#NIVEL 2 -  WRAPPER ANNOTATIONS

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
    Retrieve, update or delete a code snippet.
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


#nivel 3 -   VIEWS CLASS BASED
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



# con MIXINS

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


# con Generics

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



@permission_classes((permissions.AllowAny,))
class RegistroClienteList(APIView):
    def get(self, request, format=None):
        usuarios= User.objects.all()
        clientes = [RegistroCliente(cliente.email,"***","***") for cliente in usuarios]
        clienteSerializer = RegistroUsuarioSerializer(clientes, many=True)
        return Response(clienteSerializer.data)

    def post(self, request, format=None):
        registroUsuarioSerializer = RegistroUsuarioSerializer(data=request.data)
        if registroUsuarioSerializer.is_valid():
            registroUsuarioSerializer.save()
            return Response(registroUsuarioSerializer.data, status=status.HTTP_201_CREATED)
        return Response(registroUsuarioSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.AllowAny,))
class ValidarEmailCode(APIView):
    def post(self, request,format=None):
        """
        
        :param request: 
        :param format: 
        :return: 
        """
        return Response(request.data,status=status.HTTP_202_ACCEPTED)

    def put(self,request,format=None):
        data = request.data
        data["estado"] = "error"
        return Response(request.data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# VIEWS SETS PARA API NAVEGABLE



class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (permissions.AllowAny,)

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
    permission_classes = (permissions.AllowAny,)

class MediodepagoViewSet(viewsets.ModelViewSet):
    queryset = MedioDePago.objects.all()
    serializer_class = MedioDePagoSerializer
    permission_classes = (permissions.AllowAny,)