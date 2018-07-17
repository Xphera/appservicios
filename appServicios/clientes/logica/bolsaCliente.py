from clientes.models import (Bolsa)
from django.db.models import Sum

class BolsaCliente(object):

    def entrada(self,bolsa):
        bolsa.tipo = "entrada"
         #  guardar bolsa
        bolsa.save()

        self.calculaSaldo(bolsa)
        
    def salida(self,bolsa):
        bolsa.valor = bolsa.valor*-1
        bolsa.tipo = "salida"
         #  guardar bolsa
        bolsa.save()
        self.calculaSaldo(bolsa)

    def calculaSaldo(self,bolsa):
        # actualizacion de saldos
        bolsa.cliente.saldoBolsa = Bolsa.objects.filter(cliente = bolsa.cliente,activo=1 ).aggregate(Sum('valor'))['valor__sum']
        bolsa.cliente.save()
        if(bolsa.cliente.saldoBolsa==0):
            Bolsa.objects.filter(cliente = bolsa.cliente ).update(activo=0)


