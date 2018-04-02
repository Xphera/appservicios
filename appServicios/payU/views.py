from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (permissions,status)

from clientes.models import (Cliente)
from payU.models import TarjetaDeCredito
from servicios.models import Paquete

from payU.serializers import (
    CreateTokenSerializer,
    EliminarTokenSerializer,
    TokenSerializer,
    PaySerializer
)




# Create your views here.

@permission_classes((permissions.IsAuthenticated,))
class TarjetaCredito(APIView):

    def get(self,request,format=None):
        td = TarjetaDeCredito.objects.filter(payerId__user = request.user)
        serializer = TokenSerializer(td, many=True)      
        return Response(serializer.data)

    def post(self, request,format=None):

        data=request.data
        data["userId"] =  request.user.id

        serializer = CreateTokenSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)      
    
    def delete(self, request,id,format=None):

        try:
            td = TarjetaDeCredito.objects.get(creditCardTokenId=id, payerId__user = request.user)
            data=request.data
            data["creditCardTokenId"] = td.creditCardTokenId
            data["payerId"] = td.payerId.id

            serializer = EliminarTokenSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({"estado":"ok"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)  

        except TarjetaDeCredito.DoesNotExist:
            return Response({"error":"no existe tarjeta de crédito"}, status= status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,))
class Pay(APIView):
    def post(self, request,format=None):
       
        data=request.data
        data["user_id"] = request.user.id
        serializer = PaySerializer(data=data)

        if serializer.is_valid():
            resp = serializer.save()
            if(resp['error']== False):
                return Response(resp, status=status.HTTP_202_ACCEPTED)
            else:    
                return Response(resp, status= status.HTTP_400_BAD_REQUEST)  
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)