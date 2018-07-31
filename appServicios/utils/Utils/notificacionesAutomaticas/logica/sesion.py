from django.db.models import Q
import datetime
from datetime import timedelta
from servicios.models import CompraDetalleSesion
from utils.Utils import Utils


class sesion():
    def __init__(self, *args, **kwargs):
        self.now = datetime.datetime.now()
    def proximasesiones(self):
        #proximas - por iniciar
        prestador = []
        cliente = []        
        nowProximo = self.now+ timedelta(hours=1) 
        cds = CompraDetalleSesion.objects.filter(Q(estado_id=2) | Q(estado_id=4),Q(fechaInicio__date = nowProximo) & Q(fechaInicio__hour = nowProximo.hour))
        for s in cds:
            difference = Utils.diffTexto(s.fechaInicio,self.now)
            complemento = Utils.replaceNone(s.complemento)
            direccion = Utils.replaceNone(s.direccion)
            # cliente
            c={}
            c["titulo"]="Recordatorio de Sesión"
            c["mensaje"] = 'Próxima sesión de '+ s.compraDetalle.nombre +' en '+difference+' con '+s.compraDetalle.prestador.nombreCompleto()+' en '+direccion+' '+complemento
            c["user_id"] = s.compraDetalle.compra.cliente.user.id 
            c["app"] = 'cliente'
            c["sesion_id"]  =s.id
            c["parametros_adicionales"] = {'sesionId':c["sesion_id"],'tipo':'detalleSesionAutomatica','mensaje':c["mensaje"]}    
            cliente.append(c)
            # prestador
            p={}
            p["titulo"]="Recordatorio de Sesión"
            p["mensaje"] = 'Próxima sesión de '+ s.compraDetalle.nombre +' en '+difference+' con '+s.compraDetalle.compra.cliente.nombreCompleto()+' en '+direccion+' '+complemento
            p["user_id"] = s.compraDetalle.prestador.user.id 
            p["app"] = 'prestador'
            p["sesion_id"]  =s.id 
            p["parametros_adicionales"] = {'sesionId':p["sesion_id"],'tipo':'detalleSesionAutomatica','mensaje':p["mensaje"]}
                      
            prestador.append(p)     
        return({
            'cliente':cliente,
            'prestador':prestador
        })
    def sesionesNoIniciada(self):
        output = []           
        cds = CompraDetalleSesion.objects.filter(Q(estado_id=2) | Q(estado_id=4),Q(fechaInicio__date = self.now) & Q(fechaInicio__hour__lte = self.now.hour))
        # print(cds.query)
        for s in cds:
            complemento = Utils.replaceNone(s.complemento)
            direccion = Utils.replaceNone(s.direccion)
            o={}
            o["titulo"]="Recordatorio de Sesión"
            o["mensaje"] = 'La sesión de '+ s.compraDetalle.nombre +' con '+s.compraDetalle.compra.cliente.nombreCompleto()+' debió iniciar hace '+Utils.diffTexto(self.now,s.fechaInicio)+direccion+' '+complemento
            o["user_id"] = s.compraDetalle.prestador.user.id 
            o["app"] = 'prestador'
            o["sesion_id"]  = s.id 
            o["parametros_adicionales"] = {'sesionId':o["sesion_id"],'tipo':'detalleSesionAutomatica','mensaje':o["mensaje"]}           
            output.append(o)
        return output
