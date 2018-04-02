from rest_framework import serializers
from parametrizacion.models import (Departamento,Municipio,Sexo)


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departamento
        fields = ('id','nombre')

class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id','nombre','departamento')

class SexoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sexo
        fields = ('id','sexo')