from servicios.models import (Categoria, Servicio, Paquete, Compra)
from prestadores.models import (Prestador)
from prestadores.serializers import PrestadorSerializer
from rest_framework import serializers


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    class Meta:
        model = Categoria
        fields = ('id','nombre','detalle','imagePath','servicios')

class ServicioSerializer(serializers.HyperlinkedModelSerializer):
    #categoria = serializers.PrimaryKeyRelatedField(many=True, queryset=Categoria.objects.all())
    paquetes = serializers.PrimaryKeyRelatedField(many=True, queryset=Paquete.objects.all())
    class Meta:
        model = Servicio
        fields = ('id','categoria','categoria_id', 'nombre', 'detalle', 'imagePath','paquetes')

class PaqueteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paquete
        fields = ('id'
                  ,'servicio'
                  ,'prestador'
                  ,'nombre'
                  ,'detalle'
                  ,'cantidadDeSesiones')







class CompraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Compra
        fields= ('id','cliente','paquete','valor')

