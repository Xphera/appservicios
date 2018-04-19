from rest_framework import serializers
from prestadores.models import (Prestador,Disponibilidad)
from servicios.models import (Paquete,Servicio,CompraDetalleSesion)
from parametrizacion.serializers import MunicipioSerializer
from django.db import transaction
from datetime import date

class PrestadorSerializer(serializers.HyperlinkedModelSerializer):
    paquetes = serializers.PrimaryKeyRelatedField(many=True, queryset=Paquete.objects.all())
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    class Meta:
        model = Prestador
        
        #municipio = MunicipioSerializer(read_only=True)
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
                  ,'insignia')

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
            pk=data["sesionId"],
            estado_id=1,
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
            pk=data["sesionId"],
            estado_id=1,
            compraDetalle__estado_id = 1,
            compraDetalle__compra__cliente__user_id=data["usuarioId"]
            )
       
        if(sesion.count()==0):
            raise serializers.ValidationError({"sesionId":"Sin sesión a programar"})
        return data 