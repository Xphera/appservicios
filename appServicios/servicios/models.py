# from django.db import models
from django.contrib.gis.db import models

from django.contrib.auth.models import User


# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=20,unique=True,null=False)
    detalle = models.CharField(max_length=150,null=False)
    imagePath = models.FileField(upload_to='categorias',null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    categoria = models.ForeignKey(to='Categoria',related_name="servicios", on_delete=models.PROTECT, verbose_name="Categoria del servicio")
    nombre = models.CharField(max_length=20, unique=True, null=False)
    detalle = models.CharField(max_length=150, null=False)
    imagePath = models.FileField(upload_to='servicios', null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Paquete(models.Model):
    servicio = models.ForeignKey(to='Servicio',related_name="paquetes", on_delete=models.PROTECT)
    # prestador = models.ForeignKey(to='prestadores.Prestador',related_name="paquetes", on_delete=models.PROTECT)
    nombre = models.CharField(max_length=20, unique=True, null=False)
    detalle = models.CharField(max_length=150, null=False)
    cantidadDeSesiones = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # valor = models.FloatField()
    duracionSesion = models.IntegerField()

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    cliente  = models.ForeignKey(to='clientes.Cliente',related_name="clientes", on_delete=models.PROTECT)    
    medioPago = models.ForeignKey(to="parametrizacion.TipoMedioPago",on_delete=models.PROTECT)
    valor    = models.FloatField()
    estado  = models.ForeignKey(to="parametrizacion.EstadoCompra",on_delete=models.PROTECT)
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ( self.cliente+'-'+self.cliente+'$['+str(self.valor)+']')
    
class CompraDetalle(models.Model):
    compra  = models.ForeignKey(to='Compra', related_name='compradetalle', on_delete=models.PROTECT) 
    estado = models.ForeignKey(to="parametrizacion.EstadoCompraDetalle",related_name='estadoCompraDetalle',on_delete=models.PROTECT)
    cantidadDeSesiones = models.IntegerField()
    nombre = models.CharField(max_length=20, null=False)
    detalle = models.CharField(max_length=150, null=False)
    prestador = models.ForeignKey(to='prestadores.Prestador',related_name="compraDetalle_prestador",  on_delete=models.PROTECT)
    valor    = models.FloatField()
    paquete = models.ForeignKey(to='Paquete',related_name="compraDetalle_paquete", on_delete=models.PROTECT) 

    sesionFinalizadas    = models.IntegerField(blank=True,null=True,default=0)
    sesionAgendadas    = models.IntegerField(blank=True,null=True,default=0)
    sesionPorAgendar    = models.IntegerField(blank=True,null=True,default=0)
    duracionSesion = models.IntegerField()
    zona = models.PolygonField(blank=True,null=True)

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "CompraDetalles"

    def __str__(self):
        return ' - ('+ self.nombre+') $['+str(self.valor)+']'


class CompraDetalleSesion(models.Model):
    compraDetalle  = models.ForeignKey(to='CompraDetalle', related_name='compradetallesesiones', on_delete=models.PROTECT)
    estado = models.ForeignKey(to="parametrizacion.EstadoCompraDetalleSesion",related_name='estadoCompraDetalleSesiones',on_delete=models.PROTECT)
    calificacion = models.FloatField(default=0,null=True)
    comentario = models.CharField(blank=True,max_length=280,null=True)
    titulo = models.CharField(max_length=30,blank=True,null=True)
    direccion = models.CharField(max_length=50,blank=True,null=True)
    latitud = models.DecimalField(decimal_places=16, max_digits=21,blank=True,null=True)
    longitud = models.DecimalField(decimal_places=16, max_digits=21,blank=True,null=True)
    complemento = models.CharField(blank=True,max_length=50,null=True)
    fechaInicio = models.DateTimeField(null=True)
    fechaFin = models.DateTimeField(null=True)
    inicio = models.DateTimeField(null=True)
    fin = models.DateTimeField(null=True)

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "CompraDetallesSesiones"
        ordering = ('fechaInicio',)

        # def __str__(self):
        #     return ' - ('+self.compra.cliente.numeroDocumento+'-'+self.nombre+') $['+str(self.valor)+']'    

class CompraDetalleSesionNovedad(models.Model):
    compraDetalleSesion  = models.ForeignKey(to='CompraDetalleSesion', related_name='compradetallesesionnovedad', on_delete=models.PROTECT)
    novedad = models.CharField(max_length=200) 
    prestador = models.ForeignKey(to='prestadores.Prestador',related_name="prestadornovedad", on_delete=models.PROTECT)
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

class CompraDetalleSesionHistorico(models.Model):
    compraDetalleSesion  = models.ForeignKey(to='CompraDetalleSesion', related_name='compraDetalleSesionHistorico', on_delete=models.PROTECT)
    estado = models.ForeignKey(to="parametrizacion.EstadoCompraDetalleSesion",related_name='estadoCompraDetalleSesionesHistorico',on_delete=models.PROTECT)
    estadoNombre = models.CharField(max_length=15,null=True)    
    usuario = models.ForeignKey(to=User, related_name='usuarioDetalleSesionHistorico', on_delete=models.PROTECT, default=None, null=False)
    usuarioNombreCompleto = models.CharField(max_length=100,null=True)
    tipo =models.CharField(max_length=15) 
    created  = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('created',)

class CompraDetalleHistorico(models.Model):
    compraDetalle  = models.ForeignKey(to='CompraDetalle', related_name='compraDetalleSesionesHistorico', on_delete=models.PROTECT)
    estado = models.ForeignKey(to="parametrizacion.EstadoCompraDetalle",related_name='estadoDetalleSesionesHistorico',on_delete=models.PROTECT)
    estadoNombre = models.CharField(max_length=15,null=True)    
    usuario = models.ForeignKey(to=User, related_name='usuarioCompraDetalleSesionesHistorico', on_delete=models.PROTECT, default=None, null=False)
    usuarioNombreCompleto = models.CharField(max_length=100,null=True)
    tipo =models.CharField(max_length=15) 
    created  = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('created',)

class CompraHistorico(models.Model):
    compra  = models.ForeignKey(to='Compra', related_name='compraHistorico', on_delete=models.PROTECT)
    estado  = models.ForeignKey(to="parametrizacion.EstadoCompra",related_name='EstadoCompraHistorico',on_delete=models.PROTECT)
    estadoNombre = models.CharField(max_length=15,null=True)
    usuario = models.ForeignKey(to=User, related_name='usuarioCompraHistorico', on_delete=models.PROTECT, default=None, null=False)
    usuarioNombreCompleto = models.CharField(max_length=100,null=True)    
    tipo =models.CharField(max_length=15) 
    created  = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('created',)

class Opinion(models.Model):
    cliente = models.ForeignKey(to='clientes.Cliente', related_name="opiniones", on_delete=models.PROTECT)
    servicio = models.ForeignKey(to='Servicio', related_name="opiniones", on_delete=models.PROTECT)
    prestador = models.ForeignKey(to='prestadores.Prestador', related_name="opiniones", on_delete=models.PROTECT)
    detalle = models.TextField(max_length=250)
    created  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str({"cliente":self.cliente,"servicio":self.servicio,"prestador":self.prestador})

class Zona(models.Model):
    name = models.CharField(max_length=30)
    zona = models.PolygonField(blank=True,null=True)
    color = models.CharField(blank=True,null=True,max_length=30)
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name           