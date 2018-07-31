from servicios.models import (CompraDetalleSesion)
from django.db.models import Q

class Sesion(object):

    def detalle(self,userId,sesionId):
        sesiones = CompraDetalleSesion.objects.filter(                
                # Q(estado_id=2)|Q(estado_id=4),
                Q(compraDetalle__prestador__user_id = userId)|Q(compraDetalle__compra__cliente__user_id = userId),
                compraDetalle__estado_id = 1,                
                id = sesionId
                ).order_by('-fin').first()      
        return  sesiones 