from prestadores.models import  (Disponibilidad as Disp,Prestador)
from servicios.models import (CompraDetalleSesion)
import dateparser
from datetime import datetime, date 
import calendar
import json
from django.db.models import Q

class Sesion(object):
    #TODO: revisar parametros de entrada en metodos
    def porIniciar(self,userId):
        sesiones = CompraDetalleSesion.objects.filter(                
                Q(estado_id=2) | Q(estado_id=4),
                compraDetalle__estado_id = 1,
                fechaInicio__date = datetime.now(),
                compraDetalle__prestador__user_id = userId
                ).order_by('fechaInicio') 
        return  sesiones  
    
    def proximas(self,userId):
        sesiones = CompraDetalleSesion.objects.filter(                
                Q(estado_id=2) | Q(estado_id=4),
                compraDetalle__estado_id = 1,
                fechaInicio__date__gt = datetime.now(),
                compraDetalle__prestador__user_id = userId
                ).order_by('fechaInicio')        
        return  sesiones  

    def finalizada(self,userId):
        sesiones = CompraDetalleSesion.objects.filter(                
                Q(estado_id=3),
                compraDetalle__estado_id = 1,
                compraDetalle__prestador__user_id = userId
                ).order_by('-fin')        
        return  sesiones

    def iniciada(self,userId):
        sesiones = CompraDetalleSesion.objects.filter(                
                Q(estado_id=5),
                compraDetalle__estado_id = 1,
                compraDetalle__prestador__user_id = userId
                ).order_by('-fin')        
        return  sesiones 




