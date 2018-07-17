from rest_framework import serializers
from django.db import DatabaseError, transaction, IntegrityError
from .utils.payU import PayU
from payU.models import (TarjetaDeCredito,CobroTarjetaDeCredito,CodigoRespuetaPayu)
from clientes.models import (Cliente)
from servicios.models import (Paquete,Compra,CompraDetalle,CompraDetalleSesion)
from parametrizacion.models import (TipoMedioPago,EstadoCompra,EstadoCompraDetalle,EstadoCompraDetalleSesion)
from servicios.logica.historico import (sesionHistorico,compraDetalleHistorico,compraHistorico)
import uuid
from clientes.logica.bolsaCliente import (BolsaCliente)
from clientes.models import (Bolsa)
from payU.logica.compra import Compra

class TokenPrincipalSerializer(serializers.Serializer):
    creditCardTokenId = serializers.UUIDField()
    userId = serializers.IntegerField()

    @transaction.atomic
    def create(self, validated_data):
        try:
            tc = TarjetaDeCredito.objects.get(payerId__user__id = validated_data['userId'], creditCardTokenId=validated_data['creditCardTokenId'])
            if(tc.principal): 
                return validated_data
        except TarjetaDeCredito.DoesNotExist:
                raise serializers.ValidationError({"creditCardTokenId":"no existe tarjeta de crédito"})

        #desmarcar si existe principal        
        try: 
            tcs = TarjetaDeCredito.objects.get(payerId__user__id = validated_data['userId'],principal=True)
            tcs.principal = 0
            tcs.save()
        except Exception as e:
            print('sin principal')

        try:          
            tc.principal = 1
            tc.save()
            return validated_data
        except Exception as e:
            raise serializers.ValidationError({"error":"error"})  

    def update(self, instance, validated_data):
       return validated_data

 
class TokenSerializer(serializers.Serializer):
    creditCardTokenId = serializers.UUIDField()
    maskedNumber = serializers.CharField()
    paymentMethod = serializers.CharField()
    principal= serializers.BooleanField()


class CreateTokenSerializer(serializers.Serializer):

    userId = serializers.IntegerField()
    fullName = serializers.CharField()
    paymentMethod = serializers.CharField()
    cardNumber = serializers.IntegerField()
    expirationDate = serializers.DateField(input_formats=['%Y/%m'])
    pricipal= serializers.BooleanField(default=False)
  
    @transaction.atomic
    def create(self, validated_data):

        cliente =  Cliente.objects.get(user_id=validated_data['userId'])
        payu = PayU()

        respuesta =  payu.create_token(
                                        cliente.id,
                                        validated_data['fullName'],
                                        validated_data['paymentMethod'],
                                        validated_data['cardNumber'],
                                        validated_data['expirationDate'].strftime("%Y/%m"))

        if(respuesta.get('code') == 'SUCCESS'):

            #todo: 1) consultar si existe, y actualizar si si
            info = respuesta.get('creditCardToken')
            td = None
            try:
                td = TarjetaDeCredito.objects.get(pk = info['creditCardTokenId'])
                td.delete = False
            except Exception as e:
                td = TarjetaDeCredito()
                td.creditCardTokenId = info['creditCardTokenId']

            td.name = info['name']
            td.payerId = cliente
            td.identificationNumber = info['identificationNumber']
            td.paymentMethod = info['paymentMethod']
            td.number = info['number']
            td.expirationDate = info['expirationDate']
            td.creationDate = info['creationDate']
            td.maskedNumber = info['maskedNumber']
            
            td.save()
        else:
           raise serializers.ValidationError({"error":respuesta.get('error')})

        return validated_data

    def update(self, instance, validated_data):
       return validated_data

       
class EliminarTokenSerializer(serializers.Serializer):

    creditCardTokenId = serializers.UUIDField()
    payerId = serializers.IntegerField()

    @transaction.atomic
    def create(self, validated_data):

        payu = PayU()

        respuesta =  payu.delete_tokens(
                                        validated_data['payerId'],
                                        str(validated_data['creditCardTokenId'])
                                    )

        if(respuesta.get('code') == 'SUCCESS'): 
            td = TarjetaDeCredito()
            td.creditCardTokenId = validated_data['creditCardTokenId']   
            td.delete()
        else:
           raise serializers.ValidationError({"error":respuesta.get('error')})

        return validated_data

    def update(self, instance, validated_data):
       return validated_data


class PaySerializer(serializers.Serializer):
    #todo: revisar las fechas de inicio cuando se programe
    tokenId = serializers.UUIDField(required=False)
    cuotas = serializers.IntegerField(required=False)
    paqueteId = serializers.IntegerField()
    user_id = serializers.IntegerField()
    prestadorId = serializers.IntegerField()
    idRelacionPrestadorPaquete= serializers.IntegerField()

    def validate_cuotas(self,cuotas):
        if(cuotas < 1 or cuotas > 12):
          raise serializers.ValidationError("Número de cuotas no valido.")
        return cuotas

    def validate(self,data):
                
        if('cuotas' in data):
            if(data["cuotas"] < 1 or data["cuotas"]  > 12):
                raise serializers.ValidationError("Número de cuotas no valido.")          

        cd = CompraDetalle.objects.filter(compra__cliente__user_id=data["user_id"],estado_id=1)
        if(cd.count()>0):
            raise serializers.ValidationError({"Paquete":"el usuario cuenta con un paquete activo."})

        return data
    
    @transaction.atomic
    def create(self, validated_data):
            c = Compra(validated_data)
            return c.crear()
    def update(self, instance, validated_data):
       return validated_data
