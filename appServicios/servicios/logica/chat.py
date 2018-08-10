from  servicios.models import (CompraDetalleChat,CompraDetalleChatMensaje,CompraDetalle)
from django.contrib.auth.models import User
from utils.Utils.onesignal import Onesignal
from django.db.models import Q
from django.conf import settings

class Chat(object):

    def guardarMensaje(self,mensaje,userId,compraDetalleId):
        try:
            try:
                # existe chat
                cdc = CompraDetalleChat.objects.get(compraDetalle__id = compraDetalleId)
                cdc.save()
            except CompraDetalleChat.DoesNotExist:
                cdc = CompraDetalleChat()
                cdc.compraDetalle = CompraDetalle.objects.get(pk = compraDetalleId)
                cdc.save()

            chat = CompraDetalleChatMensaje()
            chat.compraDetalleChat = cdc            
            chat.mensaje = mensaje
            chat.usuario = User.objects.get(pk = userId)
            chat.save()
            
            if(cdc.compraDetalle.compra.cliente.user.id == userId):
                tipo = "cliente" 
            else:
                tipo = "prestador"
            # notificacion
            o = Onesignal()
            o.notificacionChat(chat,tipo)
           
            return {
                'chatId':chat.compraDetalleChat.id,
                'mensajeId':chat.id,                
                'mensaje':chat.mensaje,
                'usuarioId':chat.usuario.id,            
                'creado': str(chat.created)
                }

        except Exception as e:
            print(e)
            return False
    
    def obtenerMensaje(self,userId,compraDetalleId):
        output ={
            'mensajes':[],
        }
        try:
            chat = CompraDetalleChat.objects.get(
            Q(compraDetalle__prestador__user_id = userId)|
            Q(compraDetalle__compra__cliente__user_id = userId),
                compraDetalle__id = compraDetalleId
            )

            compraDetalle = chat.compraDetalle

            for m in chat.chatmensaje.all().order_by('created') :
                output["mensajes"].append({
                'chatId':m.compraDetalleChat.id,
                'mensajeId':m.id,
                'mensaje':m.mensaje,
                'usuarioId':m.usuario.id,            
                'creado': str(m.created)
                })

                output["compraDetalle"]={
                    'compraDetalleId':compraDetalle.id,
                    'compraDetalleEstadoId':compraDetalle.estado.id,
                    'paquete':compraDetalle.nombre,
                    'prestador':compraDetalle.prestador.nombreCompleto(),
                    'prestadorImagen': settings.MEDIA_URL+str(compraDetalle.prestador.imagePath),
                    'prestadorUserioId':compraDetalle.prestador.user.id,
                    'cliente':compraDetalle.compra.cliente.nombreCompleto(),
                    'clienteUsuarioId':compraDetalle.compra.cliente.user.id,
                    'clienteImagen': settings.MEDIA_URL+str(compraDetalle.compra.cliente.imagePath),
                }
        except CompraDetalleChat.DoesNotExist:
            compraDetalle = CompraDetalle.objects.get(
                Q(prestador__user_id = userId)|
                Q(compra__cliente__user_id = userId),
                id = compraDetalleId)

            output["compraDetalle"]={
                'compraDetalleId':compraDetalle.id,
                'compraDetalleEstadoId':compraDetalle.estado.id,
                'paquete':compraDetalle.nombre,
                'prestador':compraDetalle.prestador.nombreCompleto(),
                'prestadorImagen': settings.MEDIA_URL+str(compraDetalle.prestador.imagePath),
                'prestadorUserioId':compraDetalle.prestador.user.id,
                'cliente':compraDetalle.compra.cliente.nombreCompleto(),
                'clienteUsuarioId':compraDetalle.compra.cliente.user.id,
                'clienteImagen': settings.MEDIA_URL+str(compraDetalle.compra.cliente.imagePath)
            }
        return output
    
    def obtenerChat(self,userId):
        output = []
        chat = CompraDetalleChat.objects.filter(
           compraDetalle__prestador__user_id = userId
        ).order_by('-modified')
        try:
            if(chat.count()):        
                for c in  chat :              
                    compraDetalle = c.compraDetalle
                    output.append({
                    'chatId':c.id,
                    'paquete':compraDetalle.nombre,
                    'cliente':compraDetalle.compra.cliente.nombreCompleto(),
                    'clienteImagen': settings.MEDIA_URL+str(compraDetalle.compra.cliente.imagePath),
                    'clienteUsuarioId':compraDetalle.compra.cliente.user.id,
                    'compraDetalleId':compraDetalle.id,
                    'compraDetalleEstadoId':compraDetalle.estado.id,
                    'modificado': str(c.modified),
                    'ultimoMensaje': c.chatmensaje.latest('id').mensaje
                    })  
            return output
        except CompraDetalleChat.DoesNotExist:
            return output          
        


     



