from servicios.models import (Categoria, Servicio, Paquete, Compra,CompraDetalle,CompraDetalleSesion)
from prestadores.models import (Prestador)
from prestadores.models import (Prestador)
# from prestadores.serializers import PrestadorSerializer
from parametrizacion.models import (EstadoCompraDetalle,EstadoCompraDetalleSesion)
from parametrizacion.serializers import (EstadoCompraDetalleSesionSerializer)
from rest_framework import serializers
from django.db import transaction



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
                  ,'insignia') 


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
                    ,'sesionPorAgendadar'
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
                    ,'sesionPorAgendadar'
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

