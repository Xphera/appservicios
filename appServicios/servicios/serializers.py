from servicios.models import (Categoria, Servicio, Paquete, Compra)
from rest_framework import serializers


class CategoriaSerializer(serializers.ModelSerializer):
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    class Meta:
        model = Categoria
        fields = ('id','nombre','detalle','imagePath','servicios')

class ServicioSerializer(serializers.ModelSerializer):
    #categoria = serializers.PrimaryKeyRelatedField(many=True, queryset=Categoria.objects.all())
    class Meta:
        model = Servicio
        fields = ('id','categoria', 'nombre', 'detalle', 'imagePath',)

class PaqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Paquete
        fields = ('id','servicio','prestador','nombre','detalle','cantidadDeSesiones')

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model=Compra
        fields= ('id','cliente','paquete','valor')

