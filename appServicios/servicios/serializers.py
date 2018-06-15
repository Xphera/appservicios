from servicios.models import (Categoria, Servicio, Paquete, Compra,CompraDetalle,CompraDetalleSesion,Zona)
from prestadores.models import (Prestador)
from prestadores.models import (Prestador)
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
from dateutil.relativedelta import relativedelta
from datetime import datetime



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
                  ,'prestador'
                  ,'nombre'
                  ,'detalle'
                  ,'cantidadDeSesiones'
                  ,'valor'
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

class CompraDtllSerializer(serializers.ModelSerializer):
    compra = serializers.PrimaryKeyRelatedField(queryset=Compra.objects.all())
    estado = serializers.PrimaryKeyRelatedField(queryset=EstadoCompraDetalle.objects.all())

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

class CompraSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Compra
        fields= ('id','cliente','valor'
        ,'compradetalle'
        # ,'medioPago'
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
                if(relativedelta(sesion.fechaInicio, datetime.now()).hours < 1):
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
        except Exception as e: 
            print(e) 
            raise serializers.ValidationError("Error al guardar")  

        return validated_data

    