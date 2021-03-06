# from django.db import models
from django.contrib.gis.db import models
from parametrizacion.commonChoices import TIPO_DOCUMENTO_CHOICES
from parametrizacion.models import Municipio
from django.contrib.auth.models import User
from utils.Utils import Utils
from django.conf import settings

# Create your models here.

class Prestador(models.Model):

    nombres = models.CharField(max_length=80, verbose_name="Nombres")
    primerApellido = models.CharField(max_length=80, verbose_name="Primer Apellido")
    segundoApellido = models.CharField(max_length=80, verbose_name="Segundo Apellido")
    tipoDocumento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, verbose_name="Tipo de Documento")
    numeroDocumento = models.CharField(max_length=11, verbose_name="Numero de Documento")

    telefono = models.CharField(max_length=80, verbose_name="telefono de contacto")
    email = models.EmailField(verbose_name="Correo electronico")
    direccion = models.CharField(max_length=100)
    municipio = models.ForeignKey(to=Municipio, on_delete=models.PROTECT)

    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento")

    user = models.ForeignKey(to=User, related_name='prestadores', on_delete=models.PROTECT, default=None, null=True)

    servicios = models.ManyToManyField('servicios.Servicio' )
    
    #REVISAR OTRA VES
    # servicios = models.ForeignKey(to='servicios.Servicio', related_name='servicios_prestador', on_delete=models.PROTECT, default=None, null=True)

    perfil = models.TextField(max_length=300, verbose_name="Perfil",null=True)
    calificacion = models.CharField(max_length=2,null=True,verbose_name="Calificación")
    insignia = models.CharField(max_length=2,null=True,verbose_name="Insignia")
    profesion = models.CharField(max_length=56,null=True,verbose_name="Profesión")
    imagePath = models.FileField(upload_to="prestadores",null=True)

    zona = models.ForeignKey(to='servicios.Zona', related_name='zonas', on_delete=models.PROTECT, default=None, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def nombreCompleto(self):
        return Utils.replaceNone(self.nombres)+' '+Utils.replaceNone(self.primerApellido)+' '+Utils.replaceNone(self.segundoApellido)
    
    def obtenerImagePath(self):
       return settings.MEDIA_URL+str(self.imagePath)


    class Meta:
        verbose_name_plural = "prestadores"

    def __str__(self):
        return str({"nombre":self.nombres+" "+self.primerApellido+" "+self.segundoApellido,"documento":self.zona})

class Disponibilidad(models.Model):
    dia = models.IntegerField()
    hora = models.IntegerField()
    disponibilidad = models.BooleanField()
    prestador = models.ForeignKey(to=Prestador, on_delete=models.PROTECT)
    
class PrestadorPaquete(models.Model):
    paquete = models.ForeignKey(to='servicios.Paquete', related_name='paquetes_prestador', on_delete=models.PROTECT, default=None, null=True)
    prestador = models.ForeignKey(to='Prestador', related_name='prestador_paquetes', on_delete=models.PROTECT, default=None, null=True)
    valor = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str({"Prestador":self.prestador.nombres+" Paquete: "+self.paquete.nombre})

class Formacion(models.Model):
    prestador = models.ForeignKey(to='Prestador', related_name='prestador_formacion', on_delete=models.PROTECT, default=None, null=True)
    titulo = models.CharField(max_length=100,verbose_name="Titulo")
    institucion = models.CharField(max_length=100,verbose_name="Institucion")
    año = models.IntegerField(verbose_name="Año")
    archivoPath = models.FileField(upload_to="prestadores/formacion",null=True,verbose_name="Archivo")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Formaciones"
    def __str__(self):
        return str({"titulo":self.titulo, "Prestador":self.prestador.nombres+" "+self.prestador.primerApellido+" "+self.prestador.segundoApellido,"documento":self.prestador.numeroDocumento})
