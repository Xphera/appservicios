from django.db import models
from parametrizacion.commonChoices import TIPO_DOCUMENTO_CHOICES
from parametrizacion.models import Municipio
from django.contrib.auth.models import User
# Create your models here.

class Prestador(models.Model):

    nombres = models.TextField(max_length=80, verbose_name="Nombres")
    primerApellido = models.TextField(max_length=80, verbose_name="Primer Apellido")
    segundoApellido = models.TextField(max_length=80, verbose_name="Segundo Apellido")
    tipoDocumento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, verbose_name="Tipo de Documento")
    numeroDocumento = models.CharField(max_length=11, verbose_name="Numero de Documento")

    telefono = models.TextField(max_length=80, verbose_name="telefono de contacto")
    email = models.EmailField(verbose_name="Correo electronico")
    direccion = models.CharField(max_length=100)
    municipio = models.ForeignKey(to=Municipio, on_delete=models.PROTECT)

    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento")

    user = models.ForeignKey(to=User, related_name='prestadores', on_delete=models.PROTECT, default=None, null=True)

    servicios = models.ManyToManyField('servicios.Servicio')

    class Meta:
        verbose_name_plural = "prestadores"

    def __str__(self):
        return str({"nombre":self.nombres+" "+self.primerApellido+" "+self.segundoApellido,"documento":self.numeroDocumento})