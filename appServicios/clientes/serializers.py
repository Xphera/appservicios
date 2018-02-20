
from rest_framework import serializers
from clientes.models import (Cliente, Ubicacion, MedioDePago)
from servicios.models import (Compra)
from parametrizacion.commonChoices import TIPO_DOCUMENTO_CHOICES
from django.contrib.auth.models import User
from django.db import DatabaseError, transaction, IntegrityError

from utils.Utils.CodigosUtil import CodeFactoryUtil
from utils.Utils.MailUtil import EMAIL_TYPE, EmailFactory

"""
class ClienteSerializer_old(serializers.ModelSerializer):
    class Meta:
        model= Cliente
        user = serializers.HyperlinkedIdentityField(
            view_name='user-list')
        fields = ('id','nombres','primerApellido','segundoApellido'
                  ,'tipoDocumento','numeroDocumento','telefono','email'
                  ,'fechaNacimiento','user')


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


class RegistroUsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField()
    passw = serializers.CharField(max_length=30)
    repassw = serializers.CharField(max_length=30)
    def validate(self,data):
        if(data["passw"]!=data["repassw"]):
            raise serializers.ValidationError("eL passw y repassw deben ser identicos")

        if(User.objects.filter(username=data["email"]).exists()):
            raise serializers.ValidationError(detail="Correo electronico ya registrado", code=500)
        return data

    @transaction.atomic
    def create(self, validated_data):

        user = User.objects.create_user(validated_data["email"], password=validated_data["passw"])
        user.is_superuser = False
        user.is_staff = False
        user.email = validated_data["email"]
        user.save()


        cliente = Cliente()
        cliente.email = user.email
        cliente.user_id = user.id
        cliente.save()

        EmailFactory.getInstance(
            email_type=EMAIL_TYPE.VALIDACION_REGISTRO_CLIENTE,
            to=cliente.email,
            nombreCliente=cliente.email,
            codigoValidacion=CodeFactoryUtil.codigoValidacionEmail(cliente.email)).send()

        return validated_data

    def update(self, instance, validated_data):
        return instance

    class Meta:
        validators = []

class ValidarEmailUsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField()
    codigoValidacion = serializers.EmailField()


#SERIALIZER PARA API NAVEGABLE

class ClienteSerializer(serializers.HyperlinkedModelSerializer):

    compras = serializers.PrimaryKeyRelatedField(many=True, queryset=Compra.objects.all())
    class Meta:
        model = Cliente
        fields = ('id','nombres','primerApellido','segundoApellido'
                  ,'tipoDocumento','numeroDocumento','telefono','email'
                  ,'fechaNacimiento','user','compras')

class UbicacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ubicacion
        fields = ('id','cliente','title','direccion'
                  ,'latitud','longitud','imgPath')

class MedioDePagoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MedioDePago
        fields = ('id','tipo','franquicia','banco')
