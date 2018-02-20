from rest_framework import serializers
from parametrizacion.models import (Departamento,Municipio)


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departamento
        fields = ('id','nombre')

class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id','nombre','departamento')