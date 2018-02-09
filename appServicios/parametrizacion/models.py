from django.db import models

# Create your models here.
from django.forms.fields import CharField


class Departamento(models.Model):
    id = models.CharField(max_length=2,primary_key=True)
    nombre = models.CharField(max_length=30)

class Municipio(models.Model):
    id = models.CharField(max_length=5,primary_key=True)
    nombre = models.CharField(max_length=30)
    departamento = models.ForeignKey(to=Departamento, on_delete=models.CASCADE)