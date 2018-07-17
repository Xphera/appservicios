from servicios.models import (Categoria, Servicio, Paquete, Compra,CompraDetalle,CompraDetalleSesion,Zona,CompraDetalleSesionNovedad)
from prestadores.models import (Prestador)
# from prestadores.models import (Prestador)
# from prestadores.serializers import PrestadorSerializer
from parametrizacion.models import (EstadoCompraDetalle,EstadoCompraDetalleSesion)
from parametrizacion.serializers import (EstadoCompraDetalleSesionSerializer)
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.db import transaction
from prestadores.logica.disponibilidad import Disponibilidad
import math
import random
from django.contrib.gis.geos import (Point,Polygon)
from django.db.models import Q

from datetime import datetime
import time
from clientes.serializers import ClienteSerializer
from clientes.models import (Cliente)

from utils.Utils.onesignal import Onesignal

from servicios.logica.historico import (sesionHistorico,compraDetalleHistorico)

from  servicios.logica.paquete import Paquete as PaqueteLogica


class ZonaSerializer(GeoFeatureModelSerializer):
    id = serializers.IntegerField(read_only=True)
    color = serializers.CharField(read_only=True)
    class Meta:
        model = Zona
        geo_field = "zona"
        fields = ('zona','name','id','color')

    @transaction.atomic
    def create(self, validated_data):
        r = math.floor(random.random()*256)
        g = math.floor(random.random()*256)
        b = math.floor(random.random()*256)
        rgb = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ', 0.5)'
        try:
            z = Zona()
            z.name = validated_data["name"]
            z.zona = validated_data["zona"]
            z.color = rgb

            z.save()
        except Exception as e:  
            print(e)
            raise serializers.ValidationError("Error al guardar")  
        return validated_data

    def update(self,pk, validated_data):
        try:
            z = Zona.objects.get(pk=pk)
            z.name = validated_data["name"]
            z.zona = validated_data["zona"]
            z.save()
        except Exception as e:
            raise serializers.ValidationError("Error al guardar")  
        return validated_data  

class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    class Meta:
        model = Categoria
        fields = ('id','nombre','detalle','imagePath','servicios')

class ServicioSerializer(serializers.HyperlinkedModelSerializer):
    paquetes = serializers.PrimaryKeyRelatedField(many=True, queryset=Paquete.objects.all())
    class Meta:
        model = Servicio
        fields = ('id','categoria','categoria_id', 'nombre', 'detalle', 'imagePath','paquetes')

class PaqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paquete
        fields = ('id'
                  ,'servicio'
                #   ,'prestador'
                  ,'nombre'
                  ,'detalle'
                  ,'cantidadDeSesiones'
                #   ,'valor'
                  )

class PrestadorSerializer(serializers.ModelSerializer):
    zona = ZonaSerializer(read_only=True)
    zona_id = serializers.PrimaryKeyRelatedField(queryset=Zona.objects.all(), write_only=True, source='zonas')
    class Meta:
        model = Prestador
        fields = ('id'
                  ,'nombres'
                  ,'primerApellido'
                  ,'segundoApellido'
                  ,'perfil'
                  ,'calificacion'
                  ,'imagePath'
                  ,'profesion'
                  ,'insignia'
                  ,'zona'
                  ,'zona_id') 

class CompraSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), write_only=True, source='nombres')
    class Meta:
        model = Compra
        fields= (
            'id'
            ,'cliente'
            ,'cliente_id'
            ,'valor'
            ,'compradetalle'
        # ,'medioPago'
        )                  

class CompraDtllSerializer(serializers.ModelSerializer):
    compra = CompraSerializer(read_only=True)
    compra_id = serializers.PrimaryKeyRelatedField(queryset=Compra.objects.all(), write_only=True)

    estado = serializers.PrimaryKeyRelatedField(queryset=EstadoCompraDetalle.objects.all())

    prestador = PrestadorSerializer(read_only=True)
    prestador_id = serializers.PrimaryKeyRelatedField(queryset=Prestador.objects.all(), write_only=True, source='nombres')
        
    class Meta:
        model = CompraDetalle
        fields = (
                    'id' 
                    ,'compra'
                    ,'compra_id'
                    ,'cantidadDeSesiones'
                    ,'nombre'
                    ,'detalle'
                    ,'prestador'
                    ,'prestador_id'
                    ,'valor'
                    ,'created'
                    ,'modified'                    
                    ,'estado'
                    ,'sesionFinalizadas'
                    ,'sesionAgendadas'
                    ,'sesionPorAgendar'
                  )

class CompraDetalleSesioneSerializer(serializers.ModelSerializer):
    estado = EstadoCompraDetalleSesionSerializer(read_only=True) 
    estado_id = serializers.PrimaryKeyRelatedField(queryset=EstadoCompraDetalleSesion.objects.all(), write_only=True, source='estado')
    
    compraDetalle = CompraDtllSerializer(read_only=True)
    compraDetalle_id = serializers.PrimaryKeyRelatedField(queryset=CompraDetalle.objects.all(), write_only=True, source='compraDetalle')
    
    class Meta:
        model = CompraDetalleSesion
        fields = ('id'
                  ,'calificacion'
                  ,'titulo'
                  ,'direccion'
                  ,'latitud'
                  ,'longitud'
                  ,'complemento'
                  ,'fechaInicio'
                  ,'estado'
                  ,'estado_id'
                  ,'compraDetalle'
                  ,'compraDetalle_id'
                  ,'inicio'
                  ,'fin'
                  )               

class CompraDetalleSerializer(serializers.ModelSerializer):
    compra = serializers.PrimaryKeyRelatedField(queryset=Compra.objects.all())
    estado = serializers.PrimaryKeyRelatedField(queryset=EstadoCompraDetalle.objects.all())
    compradetallesesiones = CompraDetalleSesioneSerializer(many=True, read_only=True)

    prestador = PrestadorSerializer(read_only=True)
    prestador_id = serializers.PrimaryKeyRelatedField(queryset=Prestador.objects.all(), write_only=True, source='nombres')
        
    class Meta:
        model = CompraDetalle
        fields = (
                    'id'
                    ,'compra'
                    ,'cantidadDeSesiones'
                    ,'nombre'
                    ,'detalle'
                    ,'prestador'
                    ,'prestador_id'
                    ,'valor'
                    ,'created'
                    ,'modified'                    
                    ,'estado'
                    ,'sesionFinalizadas'
                    ,'sesionAgendadas'
                    ,'sesionPorAgendar'
                    ,'compradetallesesiones'
                  )

class CalificarSesionSerializer(serializers.Serializer):
    calificacion = serializers.IntegerField()
    comentario = serializers.CharField(allow_blank=True)
    sesionId = serializers.IntegerField()
    userId = serializers.IntegerField()

    def validate_sesionId(self,sesionId):
        sesion = CompraDetalleSesion.objects.get(pk = sesionId)
        if(sesion.calificacion >= 1):
            raise serializers.ValidationError("Sesión calificada")
        if(sesion.estado.id != 3):
            raise serializers.ValidationError("Estado de sesión no valido para calificar")    
        return sesionId

    def validate_calificacion(self,calificacion):
        if(calificacion >=1 and calificacion <=5 ):
            return calificacion
        else:
            raise serializers.ValidationError("Ingrese un valor entre 1 a 5")                               

    def validate(self,data):
        try:
            CompraDetalleSesion.objects.get(compraDetalle__compra__cliente__user_id = data["userId"],pk = data["sesionId"])
        except CompraDetalleSesion.DoesNotExist:
            raise serializers.ValidationError("No existe sesión")
        return data    

    @transaction.atomic
    def create(self, validated_data):
        try:
            cds = CompraDetalleSesion.objects.get(pk = validated_data["sesionId"])
            cds.calificacion = validated_data["calificacion"]
            cds.comentario = validated_data["comentario"]
            cds.save()
        except Exception as e:  
            raise serializers.ValidationError("Error al guardar")  

        return validated_data

class ProgramarSesionSerializer(serializers.Serializer):
    sesionId = serializers.IntegerField()
    titulo = serializers.CharField()
    complemento = serializers.CharField(allow_blank=True)
    direccion = serializers.CharField()
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    fechaInicio = serializers.DateTimeField()
    userId = serializers.IntegerField()
    estado = EstadoCompraDetalleSesionSerializer(read_only=True)

    def validate(self,data):
        sesion = CompraDetalleSesion.objects.filter(
            Q(estado_id=1) | Q(estado_id=2)  | Q(estado_id=4),
            pk = data["sesionId"],
            compraDetalle__compra__cliente__user_id = data["userId"]
            )
       
        if(sesion.count()):
            sesion = sesion.first()
            disp = Disponibilidad()
            
            if(sesion.compraDetalle.zona.contains(Point(data["longitud"], data["latitud"])) == False):
                raise serializers.ValidationError({"ubicacion":"Ubicación sin cobertura del prestador"})
 
            if(sesion.estado.id != 1 and sesion.estado.id != 2 and sesion.estado.id != 4):
                raise serializers.ValidationError({"sesionId":"El estado de la sesión no es valido para programar"})

            # aplica solo para programar 
            if(sesion.estado.id == 1):
               if(sesion.compraDetalle.sesionPorAgendar-1 < 0 or sesion.compraDetalle.sesionAgendadas+1 > sesion.compraDetalle.cantidadDeSesiones ):
                raise serializers.ValidationError({"sesion":"Sesión no valida para programar"})

            # aplica solo para reprogramar 
            if(sesion.estado.id == 2 or sesion.estado.id == 4):
                # diferncia de entre fechas en minutos.
                diff =(time.mktime(sesion.fechaInicio.timetuple())-time.mktime(datetime.now().timetuple()))/ 60         
                if(diff < 60):
                    raise serializers.ValidationError({"sesion":"Solo se puede reprogramar sesión  una hora antes de la fecha de inicio."})                
        
            if(sesion.compraDetalle.estado.id != 1):
                raise serializers.ValidationError({"estadoPaquete":"El estado del paquete no es valido para programar"})

            if(sesion.compraDetalle.compra.estado.id != 1):
                raise serializers.ValidationError({"estadoCompra":"El estado de la compra no es valido para programar"})  
        
            if(disp.validarDisponibilidadSegunSesion(data["fechaInicio"],data["sesionId"])==False):
                 raise serializers.ValidationError({"fechaInicio":"Sin disponibilidad para " +str(data["fechaInicio"]) }) 
        else:
            raise serializers.ValidationError("No existe sesión a programar")
        return data  

    @transaction.atomic
    def create(self, validated_data):
        try:
            
            cds = CompraDetalleSesion.objects.get(pk=validated_data["sesionId"])
            cds.titulo = validated_data["titulo"]
            cds.complemento = validated_data["complemento"]
            cds.direccion = validated_data["direccion"]
            cds.latitud = validated_data["latitud"]
            cds.longitud = validated_data["longitud"]
            cds.fechaInicio =validated_data["fechaInicio"]
            # solo para programar
            if(cds.estado.id == 1):
                cds.estado= EstadoCompraDetalleSesion.objects.get(pk=2)            
                cds.compraDetalle.sesionAgendadas = cds.compraDetalle.sesionAgendadas + 1
                cds.compraDetalle.sesionPorAgendar = cds.compraDetalle.sesionPorAgendar - 1
                cds.compraDetalle.save()                 
            else:
                cds.estado= EstadoCompraDetalleSesion.objects.get(pk=4)
            cds.save()
            
            # historico
            cdsh = sesionHistorico()
            cdsh.insertar(cds,validated_data["userId"]) 

            # notificación.
            o = Onesignal()
            o.notificacionSesion(cds,"prestador")

            validated_data['inicio'] = cds.inicio
            validated_data['fin'] = cds.fin
            validated_data['estado'] = cds.estado
            validated_data['estadoId'] = cds.estado.id
            validated_data['fechaInicio'] = cds.fechaInicio
            validated_data['direccion'] = cds.direccion        
            return validated_data

        except Exception as e: 
            print(e) 
            raise serializers.ValidationError("Error al guardar")  

        return validated_data

class IniciarSesionSerializer(serializers.Serializer):
    sesionId = serializers.IntegerField()
    userId = serializers.IntegerField()
    inicio = serializers.DateTimeField(required=False)
    estado = serializers.CharField(required=False)
    estadoId = serializers.IntegerField(required=False)

    def validate(self,data):
       
        sesion = CompraDetalleSesion.objects.filter(
            Q(estado_id=2)  | Q(estado_id=4),
            pk = data["sesionId"],
            compraDetalle__prestador__user_id = data["userId"] 
            )
        if(sesion.count()):
            sesion = sesion.first()
            # diferncia de entre fechas en minutos.
            diff =(time.mktime(sesion.fechaInicio.timetuple())-time.mktime(datetime.now().timetuple()))/ 60
            if(diff > 15):
                raise serializers.ValidationError({"sesion":"Solo se puede iniciar sesión 15 Minutos antes de la fecha de inicio."})
        else:
            raise serializers.ValidationError("No existe sesión a programar")
        return data

    @transaction.atomic
    def create(self, validated_data):       

        cds = CompraDetalleSesion.objects.get(pk=validated_data["sesionId"])
        cds.inicio = datetime.now()
        cds.estado= EstadoCompraDetalleSesion.objects.get(pk=5)
        cds.save()
        
        # historico        
        cdsh = sesionHistorico()
        cdsh.insertar(cds,validated_data["userId"]) 
        # output
        validated_data['inicio'] = cds.inicio
        validated_data['estado'] = cds.estado.estado
        validated_data['estadoId'] = cds.estado.id
        return validated_data

class FinalizarSesionSerializer(serializers.Serializer):
    sesionId = serializers.IntegerField()
    userId = serializers.IntegerField()
    tipo = serializers.CharField()
    novedad = serializers.CharField(required=False, max_length=200,min_length=10, allow_blank=True)
    inicio = serializers.DateTimeField(required=False)
    fin = serializers.DateTimeField(required=False)
    fechaInicio = serializers.DateTimeField(required=False)
    estado = serializers.CharField(required=False)
    estadoId = serializers.IntegerField(required=False)
    direccion = serializers.CharField(required=False)

    def validate(self,data):
        sesion = CompraDetalleSesion.objects.filter(
            Q(estado_id=5),
            pk = data["sesionId"],
            compraDetalle__prestador__user_id = data["userId"] 
            )
        if(sesion.count()):
            # sesion = sesion.first()
            if(data["tipo"] != 'sinNovedad' and data["tipo"] != 'conNovedad' and data["tipo"] != 'cancelar' ):
               raise serializers.ValidationError("Selecione un tipo valido para finalizar sesión")
            if(data["tipo"]  == 'conNovedad' and len(data["novedad"]) <= 10 ) :
               raise serializers.ValidationError("Ingresa novedad")
        else:
            raise serializers.ValidationError("No existe sesión a programar")
        return data

    @transaction.atomic
    def create(self, validated_data):
        cds = CompraDetalleSesion.objects.get(pk=validated_data["sesionId"])

        if(validated_data["tipo"]== 'sinNovedad' or validated_data["tipo"]== 'conNovedad'):
            cds.fin =  datetime.now()
            cds.estado= EstadoCompraDetalleSesion.objects.get(pk=3)
            if(validated_data["tipo"]== 'conNovedad'):
                novedad = CompraDetalleSesionNovedad()
                novedad.novedad = validated_data["novedad"]
                novedad.compraDetalleSesion = cds
                novedad.prestador = cds.compraDetalle.prestador
                novedad.save()

            cds.compraDetalle.sesionFinalizadas = cds.compraDetalle.sesionFinalizadas+1
            cds.compraDetalle.sesionAgendadas = cds.compraDetalle.sesionAgendadas-1
            cds.compraDetalle.save()
            cds.save()
            # historico
            cdsh = sesionHistorico()
            cdsh.insertar(cds,validated_data["userId"])
            # finalizar paquete.
            if(cds.compraDetalle.sesionFinalizadas == cds.compraDetalle.cantidadDeSesiones):
                cds.compraDetalle.estado = EstadoCompraDetalle.objects.get(pk=2)
                cds.compraDetalle.save()

                # historico de paquete
                cdh = compraDetalleHistorico()
                cdh.insertar(cds.compraDetalle,validated_data["userId"])
        else:

            # cancelar sesion
            cs = cancelarSesion()
            cs.cancelar(cds,validated_data)
        
        validated_data['inicio'] = cds.inicio
        validated_data['fin'] = cds.fin
        validated_data['estado'] = cds.estado.estado
        validated_data['estadoId'] = cds.estado.id
        validated_data['fechaInicio'] = cds.fechaInicio
        validated_data['direccion'] = cds.direccion

        

        
        return validated_data

class CancelarSesionSerializer(serializers.Serializer):
    sesionId = serializers.IntegerField()
    userId = serializers.IntegerField()
    inicio = serializers.DateTimeField(required=False)
    fin = serializers.DateTimeField(required=False)
    fechaInicio = serializers.DateTimeField(required=False)
    estado = EstadoCompraDetalleSesionSerializer(read_only=True)
    direccion = serializers.CharField(required=False)

    def validate(self,data):
        sesion = CompraDetalleSesion.objects.filter(
            Q(estado_id=2)  | Q(estado_id=4),
            Q(compraDetalle__prestador__user_id = data["userId"])|Q(compraDetalle__compra__cliente__user_id = data["userId"]),
            pk = data["sesionId"],             
            )

        if(sesion.count() == 0):
            raise serializers.ValidationError("No existe sesión a programar")

        # aplica solo para cliente 
        sesion = sesion.first()
        if(sesion.compraDetalle.compra.cliente.user.id == data["userId"]):
            # diferncia de entre fechas en minutos.
            diff =(time.mktime(sesion.fechaInicio.timetuple())-time.mktime(datetime.now().timetuple()))/ 60         
            if(diff < 60):
                raise serializers.ValidationError("Solo se puede cancelar sesión una hora antes de la fecha de inicio.") 

        return data

    @transaction.atomic
    def create(self, validated_data):
        cds = CompraDetalleSesion.objects.get(pk=validated_data["sesionId"])  
        cs = cancelarSesion()
        cs.cancelar(cds,validated_data)

        validated_data['inicio'] = cds.inicio
        validated_data['fin'] = cds.fin
        validated_data['estado'] = cds.estado
        validated_data['fechaInicio'] = cds.fechaInicio
        validated_data['direccion'] = cds.direccion        
        return validated_data

class CancelarPaqueteSerializer(serializers.Serializer):
    paqueteId = serializers.IntegerField()
    userId = serializers.IntegerField()
    motivoCancelacion =  serializers.CharField(max_length=200, min_length=10)

    def validate(self,data):
        paquete = CompraDetalle.objects.filter(
            estado_id=1,
            compra__cliente__user_id = data["userId"],
            pk = data["paqueteId"],             
            )

        if(paquete.count() == 0):
            raise serializers.ValidationError("No existe paquete a cancelar")

        # si hay sesion en ejecuncion
        paquete = paquete.first()
        if(paquete.compradetallesesiones.filter(estado = 5).count()):
            raise serializers.ValidationError("te encuentras en una sesión en ejecución por favor espera a terminarla para cancelar paquete.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        p = PaqueteLogica()                
        return p.cancelarPaquete(validated_data["userId"],validated_data["paqueteId"],validated_data["motivoCancelacion"])


class RenovarPaqueteSerializer(serializers.Serializer):
        compraDetalleId = serializers.IntegerField()
        userId = serializers.IntegerField()
         

# clase cancelar sesion
class cancelarSesion(object):
    def cancelar(self,cds,validated_data):
        cds.estado= EstadoCompraDetalleSesion.objects.get(pk=6)
        cds.inicio = None
        cds.fin = None
        cds.fechaInicio = None
        cds.titulo = None
        cds.longitud = None
        cds.latitud = None
        cds.direccion=None
        cds.save()

         # historico        
        cdsh = sesionHistorico()
        cdsh.insertar(cds,validated_data["userId"])
        # cambiar estado a por programar
        cds.compraDetalle.sesionPorAgendar = cds.compraDetalle.sesionPorAgendar+1
        cds.compraDetalle.sesionAgendadas = cds.compraDetalle.sesionAgendadas-1
        cds.estado= EstadoCompraDetalleSesion.objects.get(pk=1)
        cds.save()
        cds.compraDetalle.save()

        # historico        
        cdsh = sesionHistorico()
        cdsh.insertar(cds,validated_data["userId"])
