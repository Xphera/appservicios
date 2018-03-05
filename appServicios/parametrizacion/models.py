from django.db import models

# Create your models here.
from django.forms.fields import CharField


class Departamento(models.Model):
    id = models.CharField(max_length=2,primary_key=True)
    nombre = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str((self.nombre,self.id))

class Municipio(models.Model):
    id = models.CharField(max_length=5,primary_key=True)
    nombre = models.CharField(max_length=30)
    departamento = models.ForeignKey(to='Departamento', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str((self.nombre,self.id,self.departamento))


class EstadoSesion(models.Model):
    estado = models.CharField(max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.estado

class TipoDocumento(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    tipo = models.CharField(max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.tipo

class Sexo(models.Model):
    id = models.CharField(max_length=1, primary_key=True)
    sexo = models.CharField(max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.sexo

class FranquiciasTarjetasCredito(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    franquicia = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.franquicia

class TipoMedioPago(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    medioPago = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.medioPago