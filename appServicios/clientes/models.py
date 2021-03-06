from django.db import models
from parametrizacion.commonChoices import (TIPO_DOCUMENTO_CHOICES, FRANQUICIAS_CHOICES, MEDIOS_DE_PAGO_CHOICES, ESTADO_SESION_CHOICES)
from servicios.models import Compra
from utils.Utils import Utils
from django.conf import settings

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
    sexo = models.ForeignKey(to='parametrizacion.Sexo',on_delete=models.PROTECT, default=None, null=True)
    user = models.ForeignKey(to=User, related_name='clientes', on_delete=models.PROTECT, default=None, null=False)
    saldoBolsa = models.FloatField(default=0)
    activo = models.BooleanField(default=False)
    imagePath = models.FileField(upload_to="clientes",null=True)
    cuentaCerrada = models.BooleanField(default=False)
    idFb = models.CharField(max_length=80, verbose_name="idFb", null=True)
    idGoog = models.CharField(max_length=80, verbose_name="idGoog", null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def nombreCompleto(self):
        # si usuario cierra cuentas
        if(self.cuentaCerrada):
            return 'No disponible'
        else:
            return Utils.replaceNone(self.nombres)+' '+Utils.replaceNone(self.primerApellido)+' '+Utils.replaceNone(self.segundoApellido)

    def obtenerImagePath(self):
        # si usuario cierra cuentas
        if(self.cuentaCerrada):
            return settings.MEDIA_URL+'clientes/nn.PNG'
        elif(self.imagePath):
            return settings.MEDIA_URL+str(self.imagePath)
        else:                
            return settings.MEDIA_URL+'clientes/nn.PNG'

    def __str__(self):
        return str({"nombre":self.nombreCompleto(),"email":self.email,"cuentaCerrada":self.cuentaCerrada})


class Ubicacion(models.Model):
    cliente = models.ForeignKey(to='Cliente', related_name='ubicaciones', on_delete=models.PROTECT)
    departamento = models.ForeignKey(to='parametrizacion.Departamento', on_delete=models.PROTECT, null=True)
    municipio = models.ForeignKey(to='parametrizacion.Municipio', on_delete=models.PROTECT,null=True)
    titulo = models.CharField(max_length=30,default="Sin Titulo")
    direccion = models.CharField(max_length=50)
    latitud = models.DecimalField(decimal_places=16, max_digits=21)
    longitud = models.DecimalField(decimal_places=16, max_digits=21)
    imgPath = models.ImageField(default=None, null=False)
    complemento = models.CharField(blank=True,max_length=50) 

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str((self.titulo,self.direccion))

    class Meta:
        verbose_name_plural = "ubicaciones"


class MedioDePago(models.Model):
    cliente = models.ForeignKey(to='Cliente',related_name="medio_de_pago", on_delete=models.PROTECT)

    tipo = models.CharField(max_length=2, choices=MEDIOS_DE_PAGO_CHOICES)
    franquicia = models.ForeignKey(to='parametrizacion.FranquiciasTarjetasCredito', related_name="medio_de_pago",on_delete=models.PROTECT)
    banco = models.CharField(max_length=20)
    numero = models.CharField(max_length=10)
    fecha = models.DateField()
    cvv = models.CharField(max_length=3)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.franquicia+" ["+self.numero[:3]+"...]"

    class Meta:
        verbose_name_plural = "mediosDePago"

class Sesion(models.Model):
    cliente = models.ForeignKey(to='Cliente', on_delete=models.PROTECT)
    compra = models.ForeignKey(to='servicios.Compra', on_delete=models.PROTECT)
    ubicacion = models.ForeignKey(to='Ubicacion', on_delete=models.PROTECT)
    estado = models.ForeignKey(to='parametrizacion.EstadoSesion', on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str((self.cliente,self.compra))


class Bolsa(models.Model):
    cliente = models.ForeignKey(to='Cliente', on_delete=models.PROTECT)
    compraDetalle = models.ForeignKey(to='servicios.CompraDetalle',related_name="bolsaCompraDetalle",null=True, on_delete=models.PROTECT)
    compra = models.ForeignKey(to='servicios.Compra',related_name="bolsaCompra",null=True, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10)
    descripcion = models.TextField()
    valor    = models.FloatField()
    activo    = models.BooleanField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str((self.cliente,self.valor))
