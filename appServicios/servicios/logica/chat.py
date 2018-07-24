from  servicios.models import (SesionChat,CompraDetalleSesion)
from django.contrib.auth.models import User
from utils.Utils.onesignal import Onesignal
from django.db.models import Q

class Chat(object):

    def guardarMensaje(self,mensaje,userId,sesionId):
        try:
            sc = SesionChat()
            sc.mensaje = mensaje
            sc.compraDetalleSesion = CompraDetalleSesion.objects.get(pk = sesionId) 
            sc.usuario = User.objects.get(pk = userId) 
            sc.save()
                       
            if(sc.compraDetalleSesion.compraDetalle.compra.cliente.user.id == userId):
                tipo = "prestador"
            else:
                tipo = "cliente"
            # notificacion
            o = Onesignal()
            o.notificacionChat(sc,tipo)
            return True

        except Exception as e:
            print(e)
            return False
    
    def obtenerMensaje(self,userId,sesionId):
        output ={
            'mensajes':[],
        }
        sc = SesionChat.objects.filter(
           Q(compraDetalleSesion__compraDetalle__prestador__user_id = userId)|
           Q(compraDetalleSesion__compraDetalle__compra__cliente__user_id = userId),
            compraDetalleSesion__id = sesionId
        ).order_by('created')

        if(sc.count()):
            
            for m in  sc :
                output["mensajes"].append({
                'id':m.id,
                'mensaje':m.mensaje,
                'usuario':m.usuario.id,
                'sesionId':m.compraDetalleSesion.id,
                'creado': str(m.created)
                })
            sesion = sc.first().compraDetalleSesion
            output["sesion"]={
                'paquete':sesion.compraDetalle.nombre,
                'prestador':sesion.compraDetalle.prestador.nombreCompleto()
            }
        return output





     



