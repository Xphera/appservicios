from rest_framework import serializers
from parametrizacion.models import (Departamento,Municipio,Sexo,EstadoCompraDetalleSesion)


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departamento
        fields = ('id','nombre')

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id','nombre','departamento')

class SexoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sexo
        fields = ('id','sexo')

class EstadoCompraDetalleSesionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EstadoCompraDetalleSesion
        fields = ('id','estado')