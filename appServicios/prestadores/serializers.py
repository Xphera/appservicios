from rest_framework import serializers
from prestadores.models import (Prestador,Disponibilidad)
from servicios.models import (Paquete,Servicio,CompraDetalleSesion,Zona)
from servicios.serializers import (ZonaSerializer)
from parametrizacion.serializers import MunicipioSerializer
from django.db import transaction
from datetime import date
from django.db.models import Q

class PrestadorSerializer(serializers.HyperlinkedModelSerializer):
    paquetes = serializers.PrimaryKeyRelatedField(many=True, queryset=Paquete.objects.all())
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    zona = serializers.PrimaryKeyRelatedField(many=False, queryset=Zona.objects.all())

    zona = ZonaSerializer(read_only=True)
    zona_id = serializers.PrimaryKeyRelatedField(queryset=Zona.objects.all(), write_only=True, source='zonas')
    class Meta:
        model = Prestador
        fields = ('id','nombres','primerApellido','segundoApellido'
                  ,'tipoDocumento','numeroDocumento','telefono','email'
                  ,'direccion'
                  ,'municipio'
                  ,'fechaNacimiento'
                  ,'user'
                  ,'paquetes'
                  ,'servicios'
                  ,'perfil'
                  ,'calificacion'
                  ,'imagePath'
                  ,'profesion'
                  ,'insignia'
                  ,'zona'
                  ,'zona_id')

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

class zonaSerializer(serializers.Serializer):
    zonaId = serializers.IntegerField()
    usuarioId = serializers.IntegerField()
    class Meta:
        model = Prestador
        fields = ('zona')
    @transaction.atomic
    def update(self,pk,validated_data):
        z = Zona.objects.get(pk=validated_data["zonaId"])
        p = Prestador.objects.get(user_id=pk)
        p.zona = z
        p.save()
        return validated_data