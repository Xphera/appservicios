
from rest_framework import serializers
from clientes.models import Cliente
from parametrizacion.commonChoices import TIPO_DOCUMENTO_CHOICES
from django.contrib.auth.models import User
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Cliente
        user = serializers.HyperlinkedIdentityField(
            view_name='user-list')
        fields = ('id','nombres','primerApellido','segundoApellido'
                  ,'tipoDocumento','numeroDocumento','telefono','email'
                  ,'fechaNacimiento','user')
"""

class  ClienteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombres = serializers.CharField(max_length=80)
    primerApellido = serializers.CharField(max_length=80)
    segundoApellido = serializers.CharField(max_length=80)
    tipoDocumento = serializers.ChoiceField(choices=TIPO_DOCUMENTO_CHOICES)
    numeroDocumento=serializers.CharField(max_length=11)
    telefono=serializers.CharField(max_length=80)
    email=serializers.CharField(max_length=30)
    fechaNacimiento = serializers.DateField()
    user  = serializers.ModelField(model_field=User)
    def create(self, validated_data):
        return Cliente.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombres = validated_data.get('nombres',instance.nombres)
        instance.primerApellido  = validated_data.get('primerApellido', instance.primerApellido)
        instance.segundoApellido = validated_data.get('segundoApellido', instance.segundoApellido)
        instance.tipoDocumento = validated_data.get('tipoDocumento', instance.tipoDocumento)
        instance.numeroDocumento = validated_data.get('numeroDocumento', instance.numeroDocumento)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.email = validated_data.get('email', instance.email)
        instance.fechaNacimiento = validated_data.get('fechaNacimiento', instance.fechaNacimiento)
        instance.user = validated_data.get('user',instance.user)
        instance.save()
        return  instance
"""