from django.db import models
from clientes.models import Cliente

# Create your models here.
# class Tarjetas(Model.models):


class TarjetaDeCredito(models.Model):
    creditCardTokenId = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    payerId = models.ForeignKey(to=Cliente, on_delete=models.PROTECT)
    identificationNumber =  models.IntegerField(blank=True, null=True)
    paymentMethod = models.CharField(max_length=10)
    number = models.IntegerField(blank=True, null=True)
    expirationDate = models.DateField(blank=True, null=True)
    creationDate = models.CharField(max_length=50,blank=True, null=True)
    maskedNumber = models.CharField(max_length=50,blank=True, null=True)

    created = models.DateTimeField(auto_now=True)
    # created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.paymentMethod+" "+self.maskedNumber

    class Meta:
        verbose_name_plural = "tarjetasDeCredito"

class CobroTarjetaDeCredito(models.Model):
    # referenceCode = models.AutoField(primary_key=True, editable=False)
    referenceCode =  models.UUIDField(primary_key=True, editable=False)
    creditCardToken= models.ForeignKey(to=TarjetaDeCredito, on_delete=models.PROTECT)
    description =  models.TextField(blank=True, null=True)
    notifyUrl = models.CharField(blank=True, null=True,max_length=100)
    value = models.FloatField(blank=True, null=True)
    cliente = models.ForeignKey(to=Cliente, on_delete=models.PROTECT)
    cuotas = models.IntegerField(blank=True, null=True)
    code = models.CharField(blank=True, null=True,max_length=10)
    orderId = models.IntegerField(blank=True, null=True)
    state = models.CharField(blank=True, null=True,max_length=20)
    responseCode = models.CharField(blank=True, null=True,max_length=60)
    trnsancion = models.TextField(blank=True, null=True)
    compra  = models.ForeignKey(to='servicios.Compra', on_delete=models.PROTECT,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.referenceCode+" "+self.state

    class Meta:
        verbose_name_plural = "cobrosTarjetaDeCredito"    


class CodigoRespuetaPayu(models.Model):
    codigo = models.CharField(max_length=60)
    descripcion = models.TextField()
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.codigo+" "+self.descripcion