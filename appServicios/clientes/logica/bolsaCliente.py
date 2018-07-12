from clientes.models import (Bolsa)
from django.db.models import Sum

class BolsaCliente(object):
    def entrada(self,bolsa):
        bolsa.tipo = "entrada"
         #  guardar bolsa
        bolsa.save()
        # actualizacion de saldos
        bolsa.cliente.saldoBolsa = Bolsa.objects.filter(cliente = bolsa.cliente ).aggregate(Sum('valor'))['valor__sum']
        bolsa.cliente.save()   
