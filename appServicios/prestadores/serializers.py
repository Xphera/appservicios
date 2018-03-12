from rest_framework import serializers
from prestadores.models import Prestador
from servicios.models import Paquete
from servicios.models import Servicio
from parametrizacion.serializers import MunicipioSerializer

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