from django.db import models
from prestadores.models import Prestador
from clientes.models import Cliente
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=20,unique=True,null=False)
    detalle = models.CharField(max_length=150,null=False)
    imagePath = models.FileField(upload_to='media/categorias',null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    categoria = models.ForeignKey(to=Categoria,related_name="servicios", on_delete=models.PROTECT, verbose_name="Categoria del servicio")
    nombre = models.CharField(max_length=20, unique=True, null=False)
    detalle = models.CharField(max_length=150, null=False)
    imagePath = models.FileField(upload_to='media/servicios', null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Paquete(models.Model):
    servicio = models.ForeignKey(to=Servicio,related_name="paquetes", on_delete=models.PROTECT)
    prestador = models.ForeignKey(to=Prestador,related_name="paquetes", on_delete=models.PROTECT)
    nombre = models.CharField(max_length=20, unique=True, null=False)
    detalle = models.CharField(max_length=150, null=False)
    cantidadDeSesiones = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    cliente = models.ForeignKey(to=Cliente,related_name="compras", on_delete=models.PROTECT)
    paquete = models.ForeignKey(to=Paquete,related_name="compras", on_delete=models.PROTECT)
    valor = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '('+self.cliente.numeroDocumento+'-'+self.paquete.nombre+') $['+str(self.valor)+']'