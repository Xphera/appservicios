# from prestadores.models import  (Disponibilidad as Disp,Prestador)
# from servicios.models import (CompraDetalleSesion)
# import dateparser
# from datetime import datetime, date 
# import calendar
from  servicios.models import (CompraDetalle,CompraDetalleSesion)
from parametrizacion.models import (EstadoCompraDetalleSesion,EstadoCompraDetalle)
from clientes.models import (Bolsa)
from clientes.logica.bolsaCliente import (BolsaCliente)

from servicios.logica.historico import (sesionHistorico,compraDetalleHistorico)
from django.db.models import Q

class Paquete(object):

    def cancelarPaquete(self,userId,compraDetalle):
        cd = CompraDetalle.objects.get( pk=compraDetalle )
        cds = cd.compradetallesesiones.filter(Q(estado__id = 1)|Q(estado__id = 2)|Q(estado__id = 4))
        if(cds.count() > 0):

            
            # valor bolsa
            vb = cds.count()*(cd.valor/cd.cantidadDeSesiones)          

            # cancelar sesiones no finalizadas
            cds.update(estado = EstadoCompraDetalleSesion.objects.get(pk=6))

            # cancelar detalleSesion
            cd.estado = EstadoCompraDetalle.objects.get(pk=3)
            cd.save()

            # crear bolsa
            bolsa = Bolsa()    
            bolsa.valor = vb
            bolsa.compraDetalle = cd
            bolsa.cliente = cd.compra.cliente            
            bolsa.descripcion = "cancelación de paquete "+cd.nombre+" prestador "+cd.prestador.nombres+" "+cd.prestador.primerApellido+" "+cd.prestador.segundoApellido
            b=BolsaCliente()
            b.entrada(bolsa)
            
            # historico
            cdh = compraDetalleHistorico()
            cdh.insertar(cd,userId)

            # historicos
            cdsh = sesionHistorico()
            cdsh.insertar(cd.compradetallesesiones.filter(Q(estado__id = 6)),userId) 

        else:
            print("sin sesion para cancelar...")
        # cd.estado = 2
     



