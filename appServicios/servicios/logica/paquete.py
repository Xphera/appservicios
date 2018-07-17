from  servicios.models import (CompraDetalle,CompraDetalleSesion)
from parametrizacion.models import (EstadoCompraDetalleSesion,EstadoCompraDetalle)
from clientes.models import (Bolsa)
from clientes.logica.bolsaCliente import (BolsaCliente)

from prestadores.logica.logicaPrestador import LogicaPrestador

from servicios.logica.historico import (sesionHistorico,compraDetalleHistorico)
from django.db.models import Q


class Paquete(object):

    def cancelarPaquete(self,userId,compraDetalle,motivoCancelacion):
        cd = CompraDetalle.objects.get( pk=compraDetalle )
        cds = cd.compradetallesesiones.filter(Q(estado__id = 1)|Q(estado__id = 2)|Q(estado__id = 4))
        if(cds.count() > 0):

            
            # valor bolsa
            vb = cds.count()*(cd.valor/cd.cantidadDeSesiones)          

            # cancelar sesiones no finalizadas
            cds.update(estado = EstadoCompraDetalleSesion.objects.get(pk=6))

            # cancelar detalleCompra
            cd.estado = EstadoCompraDetalle.objects.get(pk=3)
            cd.motivoCancelacion = motivoCancelacion
            cd.save()

            # crear bolsa
            bolsa = Bolsa()    
            bolsa.valor = vb
            bolsa.compraDetalle = cd
            bolsa.cliente = cd.compra.cliente            
            bolsa.descripcion = "cancelación de paquete "+cd.nombre+" prestador "+cd.prestador.nombres+" "+cd.prestador.primerApellido+" "+cd.prestador.segundoApellido
            bc=BolsaCliente()
            bc.entrada(bolsa)
            
            # historico
            cdh = compraDetalleHistorico()
            cdh.insertar(cd,userId)

            # historicos
            cdsh = sesionHistorico()
            cdsh.insertar(cd.compradetallesesiones.filter(Q(estado__id = 6)),userId) 

            return True
            
        else:
            return False


    def renovarPaquete(self,userId,compraDetalleId):
        cds = CompraDetalle.objects.get(pk=compraDetalleId,compra__cliente__user_id=userId)
        errores={}
        paquete={}
        # prestador
        prestador = cds.prestador
        # paquete
        paqueteRelacion = prestador.prestador_paquetes.get(paquete=cds.paquete)
        # ubicaciones
        ubicaciones = cds.compra.cliente.ubicaciones.all()
            # validar prestador
        if(prestador.user.is_active == True):
            # prestador no disponible            
            if(cds.paquete.is_active == True):                   
                
                paquete = {
                       'id':paqueteRelacion.paquete.id,
                       'idRelacionPrestadorPaquete':paqueteRelacion.id,
                       'prestadorId': paqueteRelacion.id,
                       'nombre':paqueteRelacion.paquete.nombre,
                       'detalle':paqueteRelacion.paquete.detalle,
                       'cantidadDeSesiones':paqueteRelacion.paquete.cantidadDeSesiones,
                       'duracionSesion':paqueteRelacion.paquete.duracionSesion,
                       'valor':paqueteRelacion.valor,
                       'servicio':paqueteRelacion.paquete.servicio.nombre,
                   }  
                # cruce de ubicaciones.              
                lprestador = LogicaPrestador()
                errores["ubicacion"] = "Ubicaciones no están dentro de la zona de cobertura del prestador" 
                for ubicacion in ubicaciones:
                    if(lprestador.geolocalizarPrestador(ubicacion.longitud,ubicacion.latitud,prestador.id) == True):
                        del errores["ubicacion"]
                        break
            else:
                errores["paquete"]= "Paquete no disponible"
        else:
            errores["prestador"] = "Prestador no disponible"
        
        return {
            'errores':{
                'total':len(errores),
                'texto':errores,
            },
            'paquete':paquete
        }
       



     



