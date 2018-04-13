from rest_framework import serializers
from django.db import DatabaseError, transaction, IntegrityError
from .utils.payU import PayU
from payU.models import (TarjetaDeCredito,CobroTarjetaDeCredito,CodigoRespuetaPayu)
from clientes.models import (Cliente)
from servicios.models import (Paquete,Compra,CompraDetalle,CompraDetalleSesion)
from parametrizacion.models import (TipoMedioPago,EstadoCompra,EstadoCompraDetalle,EstadoCompraDetalleSesion)
import uuid

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
                tipoMedioPago = TipoMedioPago.objects.get(id=1)
                estadoCompra = EstadoCompra.objects.get(id=1)
                estadoCompraDetalle =  EstadoCompraDetalle.objects.get(id=1)
                estadoCompraDetalleSesion =  EstadoCompraDetalleSesion.objects.get(id=1)
            except Cliente.DoesNotExist:
                raise serializers.ValidationError({"error":"no existe cliente"})
            except TarjetaDeCredito.DoesNotExist:
                raise serializers.ValidationError({"error":"no existe tarjeta de crédito"})
            except Paquete.DoesNotExist:
                raise serializers.ValidationError({"error":"no existe paquete a comprar"})
            except TipoMedioPago.DoesNotExist:
                raise serializers.ValidationError({"error":"no existe medio de pago"})
            except EstadoCompra.DoesNotExist:
                raise serializers.ValidationError({"error":"no existe estado de compra"})
            except EstadoCompraDetalle.DoesNotExist:
                raise serializers.ValidationError({"error":"no existe estado de detalle compra"})
            except EstadoCompraDetalleSesion.DoesNotExist:
                raise serializers.ValidationError({"error":"no existe estado de detalle compra sesión"})


            compra = Compra()
            compra.cliente = cliente
            compra.valor = pq.valor
            compra.medioPago = tipoMedioPago
            compra.estado = estadoCompra
            compra.save()

            #crear paquete comprado.
            compraDt = CompraDetalle()
            compraDt.compra = compra
            compraDt.estado = estadoCompraDetalle
            compraDt.cantidadDeSesiones = pq.cantidadDeSesiones
            compraDt.detalle = pq.detalle
            compraDt.nombre = pq.nombre
            compraDt.prestador = pq.prestador
            compraDt.paquete = pq
            compraDt.valor = pq.valor
            compraDt.save()

            #compra detalle sesion
            
            bulkCompraDetalleSesion = []
            for i in range(0,compraDt.cantidadDeSesiones):
                cds = CompraDetalleSesion()
                cds.compraDetalle = compraDt
                cds.estado = estadoCompraDetalleSesion
                bulkCompraDetalleSesion.append(cds)
            CompraDetalleSesion.objects.bulk_create(bulkCompraDetalleSesion)
            
                        
            output['error'] = False
            output['compra'] = compra.id
            output['detalleCompra'] = compraDt.id
            return output

    #         ctd = CobroTarjetaDeCredito()
    #         ctd.cliente =  cliente
    #         ctd.creditCardToken = tc
    #         ctd.description = pq.nombre+" "+pq.detalle
    #         ctd.notifyUrl = "http://localhost"
    #         ctd.value = pq.valor
    #         ctd.cuotas = validated_data['cuotas'] 
    #         ctd.referenceCode = uuid.uuid1()
    #         ctd.save()
    #         try:
    #         respuesta =  payu.submit_transaction(
    #                                         str(ctd.creditCardToken.creditCardTokenId),
    #                                         str(ctd.referenceCode), # validated_data['referenceCode'],
    #                                         ctd.description, # validated_data['description'],
    #                                         ctd.notifyUrl, # validated_data['notifyUrl'],
    #                                         ctd.value, # validated_data['value'],
    #                                         ctd.cliente.email, # validated_data['email'],                                        
    #                                         ctd.creditCardToken.paymentMethod ,# validated_data['paymentMethod'],   
    #                                         ctd.cuotas # validated_data['cuotas']                                     
    #                                     ) 
    #         except Exception as e:
    #           raise serializers.ValidationError({"error":"Error conectar pasarela de pago"})

    #         ctd.code = respuesta.get('code')
    #         ctd.trnsancion = respuesta        
    #         ctd.save()
    # # crear compras si estado de transacion es APPROVED
    #         if(ctd.code ==  "SUCCESS"):

    #             transactionResponse = respuesta.get('transactionResponse')            
    #             ctd.orderId = transactionResponse['orderId']
    #             ctd.state = transactionResponse['state']
    #             ctd.responseCode = transactionResponse['responseCode']
    #             ctd.save()
    #             if(ctd.state ==  "APPROVED"):
    #                 compra = Compra()
    #                 compra.cliente = ctd.cliente
    #                 compra.valor = ctd.value
    #                 compra.medioPago = tipoMedioPago
    #                 compra.estado = estadoCompra
    #                 compra.save()

    #                 ctd.compra = compra
    #                 ctd.save()
    #                     #crear paquete comprado.
    #                 compraDt = CompraDetalle()
    #                 compraDt.compra = compra
    #                 compraDt.estado = estadoCompraDetalle
    #                 compraDt.cantidadDeSesiones = pq.cantidadDeSesiones
    #                 compraDt.detalle = pq.detalle
    #                 compraDt.nombre = pq.nombre
    #                 compraDt.prestador = pq.prestador
    #                 compraDt.paquete = pq
    #                 compraDt.valor = pq.valor
    #                 compraDt.save()
                        
    #                 output['error'] = False
    #                 output['compra'] = compra.id
    #                 output['detalleCompra'] = compraDt.id
    #             else:

    #                 try:
    #                     codigo = CodigoRespuetaPayu.objects.get(codigo=ctd.responseCode)
    #                     output["error"] = True
    #                     output["descripcion"] = codigo.descripcion
                        
    #                 except CodigoRespuetaPayu.DoesNotExist:
    #                     output["error"] = True
    #                     output["descripcion"] = "Error desconocido."           
    #         else:
                
    #             output["error"] = True
    #             output["descripcion"] = respuesta.get('error')        
        
    #         return output

    def update(self, instance, validated_data):
       return validated_data
