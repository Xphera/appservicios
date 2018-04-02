from rest_framework import serializers
from django.db import DatabaseError, transaction, IntegrityError
from .utils.payU import PayU
from payU.models import (TarjetaDeCredito,CobroTarjetaDeCredito,CodigoRespuetaPayu)
from clientes.models import (Cliente)
from servicios.models import (Paquete,Compra,CompraDetalle)
from parametrizacion.models import (TipoMedioPago,EstadoCompra,EstadoCompraDetalle)
import uuid

 
class TokenSerializer(serializers.Serializer):
    creditCardTokenId = serializers.UUIDField()
    maskedNumber = serializers.CharField()
    paymentMethod = serializers.CharField()


class CreateTokenSerializer(serializers.Serializer):

    userId = serializers.IntegerField()
    fullName = serializers.CharField()
    paymentMethod = serializers.CharField()
    cardNumber = serializers.IntegerField()
    expirationDate = serializers.DateField(input_formats=['%Y/%m'])
  
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
            info = respuesta.get('creditCardToken')

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
    tokenId = serializers.UUIDField()
    cuotas = serializers.IntegerField()
    paqueteId = serializers.IntegerField()
    user_id = serializers.IntegerField()   
    
    @transaction.atomic
    def create(self, validated_data):
        output ={}
        payu = PayU()
        try:
            cliente = Cliente.objects.get(user_id=validated_data["user_id"])
            tc =TarjetaDeCredito.objects.get(creditCardTokenId=validated_data['tokenId'], payerId__user__id = validated_data["user_id"])
            pq = Paquete.objects.get( id =  validated_data['paqueteId'] ) 

        except Cliente.DoesNotExist:
            raise serializers.ValidationError({"error":"no existe cliente"})
        except TarjetaDeCredito.DoesNotExist:
            raise serializers.ValidationError({"error":"no existe tarjeta de crédito"})
        except Paquete.DoesNotExist:
            raise serializers.ValidationError({"error":"no existe paquete a comprar"})

        ctd = CobroTarjetaDeCredito()
        ctd.cliente =  cliente
        ctd.creditCardToken = tc
        ctd.description = pq.nombre+" "+pq.detalle
        ctd.notifyUrl = "http://localhost"
        ctd.value = pq.valor
        ctd.cuotas = validated_data['cuotas'] 
        ctd.referenceCode = uuid.uuid1()
        ctd.save()

        respuesta =  payu.submit_transaction(
                                        str(ctd.creditCardToken.creditCardTokenId),
                                        str(ctd.referenceCode), # validated_data['referenceCode'],
                                        ctd.description, # validated_data['description'],
                                        ctd.notifyUrl, # validated_data['notifyUrl'],
                                        ctd.value, # validated_data['value'],
                                        ctd.cliente.email, # validated_data['email'],                                        
                                        ctd.creditCardToken.paymentMethod ,# validated_data['paymentMethod'],   
                                        ctd.cuotas # validated_data['cuotas']                                     
                                    ) 

        ctd.code = respuesta.get('code')
        ctd.trnsancion = respuesta        
        ctd.save()
    # crear compras si estado de transacion es APPROVED
        if(ctd.code ==  "SUCCESS"):

            transactionResponse = respuesta.get('transactionResponse')            
            ctd.orderId = transactionResponse['orderId']
            ctd.state = transactionResponse['state']
            ctd.responseCode = transactionResponse['responseCode']
            ctd.save()

            if(ctd.state ==  "APPROVED"):
                compra = Compra()
                compra.cliente = ctd.cliente
                compra.valor = ctd.value
                compra.medioPago = TipoMedioPago.objects.get(id=1)
                compra.estado = EstadoCompra.objects.get(id=1)
                compra.save()

                ctd.compra = compra
                ctd.save()
                #crear paquete comprado.
                compraDt = CompraDetalle()
                compraDt.compra = compra
                compraDt.estado = EstadoCompraDetalle.objects.get(id=1)
                compraDt.cantidadDeSesiones = pq.cantidadDeSesiones
                compraDt.detalle = pq.detalle
                compraDt.nombre = pq.nombre
                compraDt.prestador = pq.prestador
                compraDt.paquete = pq
                compraDt.valor = pq.valor
                compraDt.save()
                
                output['error'] = False
                output['compra'] = compra.id
                output['detalleCompra'] = compraDt.id
            else:

                try:
                    codigo = CodigoRespuetaPayu.objects.get(codigo=ctd.responseCode)
                    output["error"] = True
                    output["descripcion"] = codigo.descripcion
                    
                except CodigoRespuetaPayu.DoesNotExist:
                    output["error"] = True
                    output["descripcion"] = "Error desconocido."
           
        else:
            
            output["error"] = True
            output["descripcion"] = respuesta.get('error')
     
        return output

    def update(self, instance, validated_data):
       return validated_data
