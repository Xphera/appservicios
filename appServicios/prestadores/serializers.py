from rest_framework import serializers
from prestadores.models import (Prestador,Disponibilidad,Formacion)
from servicios.models import (Paquete,Servicio,CompraDetalleSesion,Zona)
from servicios.serializers import (ZonaSerializer,ServicioSerializer)
from parametrizacion.serializers import MunicipioSerializer
from django.db import transaction
from datetime import date
from django.db.models import Q
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from utils.Utils import Validators

class PrestadorSerializer(serializers.ModelSerializer):
    # paquetes = serializers.PrimaryKeyRelatedField(many=True, queryset=Paquete.objects.all())
    # servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    # prestador_formacion = serializers.PrimaryKeyRelatedField(many=True, queryset=Formacion.objects.all())    
    # zona = ZonaSerializer(read_only=True)
    # zona_id = serializers.PrimaryKeyRelatedField(queryset=Zona.objects.all(), write_only=True, source='zonas')

    def validate_telefono(self,telefono):
        if(not Validators.es_numero_telefonico(str(telefono))):
            raise serializers.ValidationError(detail="El número telefonico es incorrecto")
        return telefono

    class Meta:
        model = Prestador
        fields = (
                  'telefono'
                  ,'direccion' 
                  ,'fechaNacimiento'
            
                #    'id','nombres','primerApellido','segundoApellido'
                #   ,'tipoDocumento','numeroDocumento','telefono','email'
                #   ,'direccion'
                #   ,'municipio'
                #   ,'fechaNacimiento'
                #   ,'user'
                #   ,'paquetes'
                #   ,'prestador_formacion'
                #   ,'servicios'
                #   ,'perfil'
                #   ,'calificacion'
                #   ,'imagePath'
                #   ,'profesion'
                #   ,'insignia'
                #   ,'zona'
                #   ,'zona_id'
                  )

# class PrestadorSerializer(serializers.Serializer):
#     paquetes = serializers.PrimaryKeyRelatedField(many=True, queryset=Paquete.objects.all())
#     # servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
#     servicios = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all(), write_only=True,source='serviciosx')
#     servicios_id = ServicioSerializer(read_only=True)
#     # zona = ZonaSerializer(read_only=True)
#     # zona_id = serializers.PrimaryKeyRelatedField(queryset=Zona.objects.all(), write_only=True, source='zonas')
#     class Meta:
#         model = Prestador
#         fields = ('id','nombres','primerApellido','segundoApellido'
#                   ,'tipoDocumento','numeroDocumento','telefono','email'
#                   ,'direccion'
#                   ,'municipio'
#                   ,'fechaNacimiento'
#                   ,'user'
#                   ,'paquetes'
#                   ,'servicios'
#                   ,'servicios_id'
#                   ,'perfil'
#                   ,'calificacion'
#                   ,'imagePath'
#                   ,'profesion'
#                   ,'insignia'
#                 #   ,'zona'
#                 #   ,'zona_id'
#                   )



class programacionSegunSesionSerializer(serializers.Serializer):
    sesionId = serializers.IntegerField()
    usuarioId = serializers.IntegerField()
    fechaInicio = serializers.DateField()
    
    def validate_fechaInicio(self,fechaInicio):
        now = date.today()
        if(fechaInicio < now):
            raise serializers.ValidationError("La fecha de inicio no puede menor a la fecha actual")
        return fechaInicio

    def validate(self,data):
        sesion = CompraDetalleSesion.objects.filter(
            Q(estado_id=1) | Q(estado_id=2) | Q(estado_id=4),
            pk=data["sesionId"],
            # estado_id=1,
            compraDetalle__estado_id = 1,
            compraDetalle__compra__cliente__user_id=data["usuarioId"]
            )
       
        if(sesion.count()==0):
            raise serializers.ValidationError({"sesionId":"Sin sesión a programar"})
        return data    

class disponibilidadMesSerializer(serializers.Serializer):
    sesionId = serializers.IntegerField()
    usuarioId = serializers.IntegerField()

    def validate(self,data):
        sesion = CompraDetalleSesion.objects.filter(
            Q(estado_id=1) | Q(estado_id=2) | Q(estado_id=4),
            pk=data["sesionId"],
            # estado_id=1,
            compraDetalle__estado_id = 1,
            compraDetalle__compra__cliente__user_id=data["usuarioId"]
            )

        if(sesion.count()==0):
            raise serializers.ValidationError({"sesionId":"Sin sesión a programar"})
        return data 

class zonaSerializer(GeoFeatureModelSerializer):    
    zonaId = serializers.IntegerField(write_only=True)
    usuarioId = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    color = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    class Meta:
        model = Zona
        geo_field = "zona"
        fields = ('zona','name','id','color','zonaId','usuarioId')
    @transaction.atomic
    def create(self,validated_data):
        z = Zona.objects.get(pk=validated_data["zonaId"])
        p = Prestador.objects.get(user_id=validated_data["usuarioId"])
        p.zona = z
        p.save()
        return validated_data