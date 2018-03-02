
from rest_framework import serializers
from parametrizacion.models import Sexo
from clientes.models import (Cliente, Ubicacion, MedioDePago)
from servicios.models import Compra
from parametrizacion.commonChoices import TIPO_DOCUMENTO_CHOICES
from django.contrib.auth.models import User
from django.db import DatabaseError, transaction, IntegrityError

from utils.Utils.CodigosUtil import CodeFactoryUtil
from utils.Utils import Validators
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

''' --------------------------------------------------------------------------------------------------------------  '''

class RegistroUsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField()
    passw = serializers.CharField(max_length=30)
    repassw = serializers.CharField(max_length=30)
    def validate(self,data):
        if(data["passw"]!=data["repassw"]):
            raise serializers.ValidationError("eL passw y repassw deben ser identicos")
        return data

    def validate_email(self,email):
        if(User.objects.filter(username=email).exists()):
            raise serializers.ValidationError(detail="Correo electronico ya registrado", code=500)
        return email

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

''' --------------------------------------------------------------------------------------------------------------  '''

class ValidarEmailUsuarioSerializer(serializers.Serializer):
    '''
    HUC011 - Ingresar el codigo de validacion de cambio de correo.
    '''
    email = serializers.EmailField()
    codigoValidacion = serializers.CharField(max_length=7)

    def validate_email(self,email):
        if ( not User.objects.filter(username=email).exists()):
            raise serializers.ValidationError(detail="Correo electronico no esta registrado", code=500)
        return email

    def validate(self,data):
        if (CodeFactoryUtil.codigoValidacionEmail(data["email"])!=data["codigoValidacion"]):
            raise serializers.ValidationError(detail="El codigo de validacion no corresponde", code=500)
        return data


    @transaction.atomic
    def create(self, validated_data):

        #Activar Usuario por validacion exitosa
        
        user = User.objects.get(email=validated_data["email"])
        user.is_active = True
        user.save()

        cliente = Cliente.objects.get(email=validated_data["email"])
        cliente.activo = True
        cliente.save()

        return validated_data


''' --------------------------------------------------------------------------------------------------------------  '''

class RegistrarInformacionBasicaSerializer(serializers.Serializer):
    '''
    HUC008 - Registro de informacion adicional
    '''
    email = serializers.EmailField()
    tipoDocumento = serializers.ChoiceField(choices=TIPO_DOCUMENTO_CHOICES,allow_null=True)
    numeroDocumento = serializers.CharField(max_length=11,allow_null=True)
    nombres = serializers.CharField(max_length=80,allow_null=True)
    primerApellido = serializers.CharField(max_length=80,allow_null=True)
    segundoApellido = serializers.CharField(max_length=80,allow_null=True)
    telefonoContacto = serializers.CharField(max_length=80,allow_null=True)
    fechaNacimiento = serializers.DateField(allow_null=True)
    sexo = serializers.PrimaryKeyRelatedField(queryset=Sexo.objects.all())
    def validate_tipoDocumento(self,tipo):

        TIPO_DOCUMENTOS_KEYS = [tipo[0] for tipo in TIPO_DOCUMENTO_CHOICES]
        if(tipo not in TIPO_DOCUMENTOS_KEYS):
            raise serializers.ValidationError(detail="El tipo de documento no es valido")
        return tipo

    def validate_nombres(self,nombre):
        if (not Validators.es_alfanumerico(nombre, espacios=True)):
            raise serializers.ValidationError(detail="solo se permiten valores alfanumerico")
        return nombre

    def validate_primerApellido(self, primerApellido):
        if (not Validators.es_alfanumerico(primerApellido)):
            raise serializers.ValidationError(detail="solo se permiten valores alfanumerico")
        return primerApellido

    def validate_segundoApellido(self, segundoApellido):
        if (not Validators.es_alfanumerico(segundoApellido)):
            raise serializers.ValidationError(detail="solo se permiten valores alfanumerico")
        return segundoApellido

    def validate_fechaNacimiento(self, fechaNacimiento):
        if(not Validators.menor_que_fecha_actual(fechaNacimiento)):
            raise serializers.ValidationError(detail="La fecha de Nacimiento debe ser Menor que la fecha Actual")
        return fechaNacimiento
    def validate_telefonoContacto(self,telefono):
        if(not Validators.es_numero_telefonico(str(telefono))):
            raise serializers.ValidationError(detail="El número telefonico es incorrecto")
        return telefono

    def validate_sexo(self,sexo):
        SEXO_KEYS = [sex[0] for sex in SEXO_CHOICES]
        if (sexo not in SEXO_KEYS):
            raise serializers.ValidationError(detail="El sexo no es valido")
        return sexo

    def validate_email(self, email):
        try:
            Cliente.objects.get(email=email)
        except:
            raise serializers.ValidationError(detail="El correo electronico suministrado no corresponde a ningun cliente registrado")
        return email

    @transaction.atomic
    def create(self, validated_data):
        try:
            cliente = Cliente.objects.get(email=validated_data["email"])
            cliente.activo = True
            cliente.save()
        except Cliente.DoesNotExist:
            print("No existe el cliente")
            return None
        return validated_data

    def update(self,element, validated_data):
        return validated_data

''' --------------------------------------------------------------------------------------------------------------  '''
#SERIALIZER PARA API NAVEGABLE
''' --------------------------------------------------------------------------------------------------------------  '''

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
        fields = ('id', 'cliente', 'title', 'direccion', 'latitud', 'longitud', 'imgPath')

class MedioDePagoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MedioDePago
        fields = ('id','tipo','franquicia','banco')
