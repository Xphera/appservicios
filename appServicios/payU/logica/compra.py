from rest_framework import serializers
from django.db import DatabaseError, transaction, IntegrityError
from payU.utils.payU import PayU
from payU.models import (TarjetaDeCredito,CobroTarjetaDeCredito,CodigoRespuetaPayu)
from clientes.models import (Cliente)
from servicios.models import (Paquete,Compra as CompraModel,CompraDetalle,CompraDetalleSesion)
from parametrizacion.models import (TipoMedioPago,EstadoCompra,EstadoCompraDetalle,EstadoCompraDetalleSesion)
from servicios.logica.historico import (sesionHistorico,compraDetalleHistorico,compraHistorico)
import uuid
from clientes.logica.bolsaCliente import (BolsaCliente)
from clientes.models import (Bolsa)
import json
from rest_framework.reverse import reverse

class Compra(object):

    def __init__(self, validated_data):

        try:
            self.validated_data = validated_data
            

            self.pq = Paquete.objects.get( id =  self.validated_data['paqueteId'], paquetes_prestador__paquete_id = self.validated_data['paqueteId'],paquetes_prestador__id = self.validated_data["idRelacionPrestadorPaquete"]  ) 
                    
            #relacion entre paquetes y prestador
            self.prestadorPaquete = self.pq.paquetes_prestador.get(id= self.validated_data['idRelacionPrestadorPaquete'])
            self.cliente = Cliente.objects.get(user_id=self.validated_data["user_id"])
            self.estadoCompra = EstadoCompra.objects.get(id=1)
            self.estadoCompraDetalle =  EstadoCompraDetalle.objects.get(id=1)
            self.estadoCompraDetalleSesion =  EstadoCompraDetalleSesion.objects.get(id=1)
           
            self.user_id= self.validated_data["user_id"]

            if('cuotas' in self.validated_data):
                self.cuotas = self.validated_data['cuotas'] 
            if('tokenId' in self.validated_data):
                self.creditCardTokenId = self.validated_data['tokenId']

                        
            self.nuevaCompra = CompraModel()
            self.ctc = CobroTarjetaDeCredito()
            self.payu = PayU()
            self.tipoMedioPago = TipoMedioPago()
            self.output ={}

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


    def crear(self):        
            self.medioPago()
            if(self.tipoMedioPago.id == '1'):
                # self.tipoMedioPago = TipoMedioPago.objects.get(id=1)
                value = self.prestadorPaquete.valor
                self. pagoPayU(value)

            elif(self.tipoMedioPago.id == '3'):
                # self.tipoMedioPago = TipoMedioPago.objects.get(id=3)
                value = self.prestadorPaquete.valor-self.cliente.saldoBolsa
                self.pagoPayU(value)

                if(self.ctc.state ==  "APPROVED"):
                    # crear bolsa
                    bolsa = Bolsa()    
                    bolsa.valor = self.cliente.saldoBolsa
                    bolsa.cliente = self.cliente  
                    bolsa.descripcion = "compra paquete "+self.pq.nombre+" prestador "+self.prestadorPaquete.prestador.nombres+" "+self.prestadorPaquete.prestador.primerApellido+" "+self.prestadorPaquete.prestador.segundoApellido
                    bolsa.compra= self.nuevaCompra             
                    bc=BolsaCliente()
                    bc.salida(bolsa)
            else:
                # self.tipoMedioPago = TipoMedioPago.objects.get(id=2)
                self.procesarCompra()
                # crear bolsa
                bolsa = Bolsa()    
                bolsa.valor = self.prestadorPaquete.valor
                bolsa.cliente = self.cliente  
                bolsa.descripcion = "compra paquete "+self.pq.nombre+" prestador "+self.prestadorPaquete.prestador.nombres+" "+self.prestadorPaquete.prestador.primerApellido+" "+self.prestadorPaquete.prestador.segundoApellido
                bolsa.compra= self.nuevaCompra
                bc=BolsaCliente()
                bc.salida(bolsa)

            return self.output
    def pagoPayUConfirmacion(self,ctc,confirmacion):          
            if(ctc.confirmacion == None or ctc.confirmacion == ""):
               
                # pendiente y aprobado
                if(ctc.state == 'PENDING' and confirmacion["response_message_pol"] == 'APPROVED'):
                    self.medioPago()
                            
                    self.procesarCompra()
                    # guardar numero de compra en cobro de tarjeta de credito
                    ctc.compra = self.nuevaCompra

                ctc.confirmacion = json.dumps(confirmacion)
                ctc.state = confirmacion["response_message_pol"]
                ctc.save()

    def pagoPayU(self,value):
        value = round(value,2)
        self.tc =TarjetaDeCredito.objects.get(creditCardTokenId=self.creditCardTokenId, payerId__user__id =self.user_id)
        self.ctc = CobroTarjetaDeCredito()
        self.ctc.cliente =  self.cliente
        self.ctc.creditCardToken = self.tc
        self.ctc.description = self.pq.nombre+" "+self.pq.detalle
        self.ctc.notifyUrl = "http://18.223.121.206:82/api/clientes/PayConfirmacion/"
        self.ctc.value = value
        self.ctc.cuotas = self.cuotas
        self.ctc.referenceCode = uuid.uuid1()
        self.ctc.save()
         
        
       
        try:
            respuesta =  self.payu.submit_transaction(
                                        str(self.ctc.creditCardToken.creditCardTokenId),
                                        str(self.ctc.referenceCode), # validated_data['referenceCode'],
                                        self.ctc.description, # validated_data['description'],
                                        self.ctc.notifyUrl, # validated_data['notifyUrl'],
                                        self.ctc.value, # validated_data['value'],
                                        self.ctc.cliente.email, # validated_data['email'],                                        
                                        self.ctc.creditCardToken.paymentMethod ,# validated_data['paymentMethod'],   
                                        self.ctc.cuotas # validated_data['cuotas']                                     
                                    ) 
        except Exception as e:
            raise serializers.ValidationError({"error":"Error conectar pasarela de pago"})
            
        self.ctc.code = respuesta.get('code')
        self.ctc.transancion = respuesta        
        self.ctc.datos = {}   
        # self.ctc.datos = json.dumps(self.validated_data)
        for data in self.validated_data:            
            if (type(self.validated_data[data])==uuid.UUID):
                self.ctc.datos[data] = self.validated_data[data].hex
            else:
                self.ctc.datos[data] = self.validated_data[data]    

        self.ctc.save()

        # crear compras si estado de transacion es APPROVED
        if(self.ctc.code ==  "SUCCESS"):
            transactionResponse = respuesta.get('transactionResponse')            
            self.ctc.orderId = transactionResponse['orderId']
            self.ctc.state = transactionResponse['state']
            self.ctc.responseCode = transactionResponse['responseCode']
            self.ctc.save()
            if(self.ctc.state ==  "APPROVED"):
                self.procesarCompra()
                # guardar numero de compra en cobro de tarjeta de credito
                self.ctc.compra = self.nuevaCompra
                self.ctc.save()
            else:
                try:
                    codigo = CodigoRespuetaPayu.objects.get(codigo=self.ctc.responseCode)
                    self.output["error"] = True
                    self.output["descripcion"] = codigo.descripcion
                    
                except CodigoRespuetaPayu.DoesNotExist:
                    self.output["error"] = True
                    self.output["descripcion"] = "Error desconocido."
        else:                
            self.output["error"] = True
            self.output["descripcion"] = respuesta.get('error')        
    def procesarCompra(self):
                
                self.nuevaCompra = CompraModel()
                self.nuevaCompra.cliente = self.cliente
                # valor de compra
                self.nuevaCompra.valor = self.prestadorPaquete.valor
                self.nuevaCompra.medioPago = self.tipoMedioPago
                self.nuevaCompra.estado = self.estadoCompra
                self.nuevaCompra.save()

                # historico
                ch = compraHistorico()
                ch.insertar(self.nuevaCompra,self.user_id)                
   
                #crear paquete comprado.
                compraDt = CompraDetalle()
                compraDt.compra = self.nuevaCompra
                compraDt.estado = self.estadoCompraDetalle
                compraDt.cantidadDeSesiones = self.pq.cantidadDeSesiones
                compraDt.detalle = self.pq.detalle
                compraDt.nombre = self.pq.nombre
                compraDt.prestador = self.prestadorPaquete.prestador
                compraDt.paquete = self.pq
                compraDt.valor = self.prestadorPaquete.valor
                compraDt.duracionSesion = self.pq.duracionSesion
                compraDt.sesionPorAgendar = self.pq.cantidadDeSesiones
                compraDt.zona = self.prestadorPaquete.prestador.zona.zona
                compraDt.save()

                # historico
                cdh = compraDetalleHistorico()
                cdh.insertar(compraDt,self.user_id)

                #compra detalle sesion
                bulkCompraDetalleSesion = []
                for i in range(0,compraDt.cantidadDeSesiones):
                    cds = CompraDetalleSesion()
                    cds.compraDetalle = compraDt
                    cds.estado = self.estadoCompraDetalleSesion
                    bulkCompraDetalleSesion.append(cds)
                CompraDetalleSesion.objects.bulk_create(bulkCompraDetalleSesion)

                # historico
                cdsh = sesionHistorico()
                cdsh.insertar(CompraDetalleSesion.objects.filter(compraDetalle=compraDt),self.user_id)    
                                                           
                self.output['error'] = False
                self.output['compra'] = self.nuevaCompra.id
                self.output['detalleCompra'] = compraDt.id




    def medioPago(self): 
        if(self.cliente.saldoBolsa == 0):
            self.tipoMedioPago = TipoMedioPago.objects.get(id=1)
        elif(self.prestadorPaquete.valor > self.cliente.saldoBolsa):
            self.tipoMedioPago = TipoMedioPago.objects.get(id=3)               
        else:
            self.tipoMedioPago = TipoMedioPago.objects.get(id=2)  