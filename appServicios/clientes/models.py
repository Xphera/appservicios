from django.db import models
from parametrizacion.models import Municipio
from parametrizacion.commonChoices import (TIPO_DOCUMENTO_CHOICES, FRANQUICIAS_CHOICES, MEDIOS_DE_PAGO_CHOICES)

from django.contrib.auth.models import User
# Create your models here.

class Cliente(models.Model):
    nombres = models.CharField(max_length=80, verbose_name="Nombres", null=True)
    primerApellido = models.CharField(max_length=80, verbose_name="Primer Apellido", null=True)
    segundoApellido = models.CharField(max_length=80, verbose_name="Segundo Apellido", null=True)
    tipoDocumento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, verbose_name="Tipo de Documento", null=True)
    numeroDocumento = models.CharField(max_length=11, verbose_name="Numero de Documento", null=True)

    telefono = models.CharField(max_length=80, verbose_name="telefono de contacto", null=True)
    email = models.EmailField(verbose_name="Correo electronico")

    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True)

    user = models.ForeignKey(to=User, related_name='clientes', on_delete=models.PROTECT, default=None, null=False)

    def nombreCompleto(self):
        return self.nombres+" "+self.primerApellido+" "+self.segundoApellido

    def __str__(self):
        return str({"nombre":self.nombreCompleto(),"email":self.email})


class Ubicacion(models.Model):
    cliente = models.ForeignKey(to=Cliente, on_delete=models.PROTECT)
    title = models.CharField(max_length=30,default="Sin Titulo")
    direccion = models.CharField(max_length=30)
    latitud = models.IntegerField()
    longitud = models.IntegerField()
    imgPath = models.ImageField()

    def __str__(self):
        return str((self.title,self.direccion))

    class Meta:
        verbose_name_plural = "ubicaciones"


class MedioDePago(models.Model):
    cliente = models.ForeignKey(to=Cliente, on_delete=models.PROTECT)

    tipo = models.CharField(max_length=2, choices=MEDIOS_DE_PAGO_CHOICES)
    franquicia = models.CharField(max_length=3, choices=FRANQUICIAS_CHOICES)
    banco = models.CharField(max_length=20)
    numero = models.CharField(max_length=10)
    fecha = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.franquicia+" ["+self.numero[:3]+"...]"

    class Meta:
        verbose_name_plural = "mediosDePago"
