
from servicios.models import  (CompraDetalleSesionHistorico,CompraDetalleHistorico,CompraHistorico )
from collections import Iterable

class sesionHistorico(object):
    def insertar(self,compraDetalleSesion,userId):
       
        if(isinstance(compraDetalleSesion, Iterable)):
            bulkSesion = []
            for sesion in compraDetalleSesion:
                cdsh = CompraDetalleSesionHistorico()
                cdsh.compraDetalleSesion = sesion
                cdsh.estado = sesion.estado                
                cdsh.estadoNombre = sesion.estado.estado 
                              
                if(sesion.compraDetalle.compra.cliente.user.id == userId):
                    cdsh.tipo = 'cliente'
                    cdsh.usuario = sesion.compraDetalle.compra.cliente.user
                    cdsh.usuarioNombreCompleto = sesion.compraDetalle.compra.cliente.nombreCompleto()
                elif(sesion.compraDetalle.prestador.user.id == userId):
                    cdsh.tipo = 'pestador'
                    cdsh.usuario = sesion.compraDetalle.prestador.user 
                    cdsh.usuarioNombreCompleto = sesion.compraDetalle.prestador.nombreCompleto()      
                bulkSesion.append(cdsh)
                           
            CompraDetalleSesionHistorico.objects.bulk_create(bulkSesion)
        else:
            cdsh = CompraDetalleSesionHistorico()
            cdsh.compraDetalleSesion = compraDetalleSesion
            cdsh.estado = compraDetalleSesion.estado            
            cdsh.estadoNombre = compraDetalleSesion.estado.estado

            if(compraDetalleSesion.compraDetalle.compra.cliente.user.id == userId):
                cdsh.tipo = 'cliente'
                cdsh.usuario = compraDetalleSesion.compraDetalle.compra.cliente.user
                cdsh.usuarioNombreCompleto =  compraDetalleSesion.compraDetalle.compra.cliente.nombreCompleto()
            elif(compraDetalleSesion.compraDetalle.prestador.user.id == userId):
                cdsh.tipo = 'prestador'
                cdsh.usuario = compraDetalleSesion.compraDetalle.prestador.user 
                cdsh.usuarioNombreCompleto= compraDetalleSesion.compraDetalle.prestador.nombreCompleto()
            cdsh.save()

class compraDetalleHistorico(object):
    def insertar(self,compraDetalle,userId):
        cdh = CompraDetalleHistorico()
        cdh.compraDetalle = compraDetalle
        cdh.estado = compraDetalle.estado
        cdh.estadoNombre = compraDetalle.estado.estado

        if(compraDetalle.compra.cliente.user.id == userId):
            cdh.tipo = 'cliente'
            cdh.usuario = compraDetalle.compra.cliente.user
            cdh.usuarioNombreCompleto =  compraDetalle.compra.cliente.nombreCompleto()
        elif(compraDetalle.prestador.user.id == userId):
            cdh.tipo = 'prestador'
            cdh.usuario = compraDetalle.prestador.user 
            cdh.usuarioNombreCompleto = compraDetalle.prestador.nombreCompleto()        
        cdh.save()

class compraHistorico(object):
    def insertar(self,compra,userId):
        ch = CompraHistorico()        
        ch.compra = compra
        ch.estado = compra.estado
        ch.estadoNombre = compra.estado.estado
        
        if(compra.cliente.user.id == userId):
            ch.tipo = 'cliente'
            ch.usuario = compra.cliente.user
            ch.usuarioNombreCompleto =  compra.cliente.nombreCompleto()
        ch.save()        
       