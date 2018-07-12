from rest_framework import serializers
from rest_framework.authtoken.models import Token 
from utils.Utils.CodigosUtil import CodeFactoryUtil
from utils.Utils import Validators
from utils.Utils.MailUtil import EMAIL_TYPE, EmailFactory
from django.db import DatabaseError, transaction, IntegrityError
from django.contrib.auth.models import User
from clientes.models import (Cliente)
from prestadores.models import (Prestador)

class Usuario(object):
    def cambioContrenia(self,request):
        output={}
        serializer = CambiarPasswordSerializer(data=request.data)
        if serializer.is_valid():        
            if not request.user.check_password(serializer.data.get("password")):
                output["estado"]=False
                output["error"]=["Contraseña incorrecta."]
                return output                    
            
            request.user.set_password(serializer.data.get("newpassword"))
            request.user.save()
            Token.objects.get(user=request.user).delete()
            token = Token.objects.create(user=request.user)
            output["estado"]=True
            output["token"]=token.key
            return output
        else:
            output["estado"]=False
            output["error"]=serializer.errors
            return output

    def cambioUsuario(self,request):
        output={}
        data=request.data
        data['user_id']=request.user.id
        serializer = CambiarUsuarioSerializer(data=data)
        if serializer.is_valid():
            if not request.user.check_password(request.data['password']):
                output["estado"]=False
                output["error"]=["Contraseña incorrecta."]               
            else:
                serializer.save()
                output["estado"]=True
                return output
        else:
            output["estado"]=False
            output["error"]=serializer.errors
            return output

    def cambioUsuarioValidarCodigo(self,request):
        output={}
        data=request.data
        data['user_id'] = request.user.id
        serializer = CambiarUsuarioValidarCodigoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            Token.objects.get(user=request.user).delete()
            token = Token.objects.create(user=request.user)
            output["estado"]=True
            output["token"]=token.key
            return output
        else:
            output["estado"]=False
            output["error"]=serializer.errors
            return output  

    def restablecerPassword(self,request):
        output={}
        data=request.data
        serializer = RestablecerPassword(data=data)
        if serializer.is_valid():
            output["estado"]=True
            serializer.save()
            return output         
        else:
            output["estado"]=False
            output["error"]=serializer.errors
            return output

    def restablecerPasswordValidaCodigo(self,request):
        output={}
        data=request.data
        serializer = RestablecerPasswordValidaCodigo(data=data)
        if serializer.is_valid():
            usuario = User.objects.get(username=serializer.data.get("usuario"))
            usuario.set_password(serializer.data.get("password"))
            usuario.save()
            Token.objects.get(user=usuario).delete()
            token = Token.objects.create(user=usuario)
            output["estado"]=True
            output["token"]=token.key
            return output       
        else:
            output["estado"]=False
            output["error"]=serializer.errors
            return output



# serializadores....................................
class CambiarPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)
    newpassword = serializers.CharField( max_length=30)
    repeatnewpassword = serializers.CharField( max_length=30)

    def validate(self,data):
        if(data["newpassword"]!=data["repeatnewpassword"]):
            raise serializers.ValidationError({"newpassword":"La nueva contraseña y su confirmación no coinciden"})
        return data

class RestablecerPasswordValidaCodigo(serializers.Serializer):
    usuario = serializers.CharField(max_length=30)
    codigo = serializers.CharField()
    password = serializers.CharField()
    repeatpassword = serializers.CharField()

    def validate_usuario(self,usuario):
        if (User.objects.filter(username=usuario).exists() == False):
            raise serializers.ValidationError(["Usuario no registrado"])
        return usuario

    def validate(self,data):
        if (CodeFactoryUtil.codigoValidacionEmail(data["usuario"])!= data["codigo"]):
            raise serializers.ValidationError(["El codigo de validacion no corresponde"])

        if(data["password"]!=data["repeatpassword"]):
            raise serializers.ValidationError(["La nueva contraseña y su confirmación no coinciden"])
        return data

class RestablecerPassword(serializers.Serializer):
    usuario = serializers.CharField( max_length=30)

    def validate_usuario(self,usuario):
        if (User.objects.filter(username=usuario).exists() == False):
            raise serializers.ValidationError(["Usuario no registrado"])
        return usuario
    @transaction.atomic
    def create(self, validated_data): 
        usuario = User.objects.get(username=validated_data['usuario'])
        email = validated_data['usuario']
        EmailFactory.getInstance(
        email_type=EMAIL_TYPE.VALIDACION_REGISTRO_CLIENTE,
        to= email,
        nombreCliente=usuario.first_name+''+usuario.last_name,
        codigoValidacion=CodeFactoryUtil.codigoValidacionEmail(email)).send()
        return validated_data

class CambiarUsuarioSerializer(serializers.Serializer):
    newusuario = serializers.EmailField()
    password = serializers.CharField()
    user_id = serializers.IntegerField()

    def validate_newusuario(self,newusuario):
        if(User.objects.filter(username=newusuario).exists()):
            raise serializers.ValidationError({"usuario":["Usuario ya registrado"]})
        return newusuario

    @transaction.atomic
    def create(self, validated_data): 
        usuario = User.objects.get(id=validated_data['user_id'])
        email = validated_data['newusuario']
        EmailFactory.getInstance(
        email_type=EMAIL_TYPE.VALIDACION_REGISTRO_CLIENTE,
        to= email,
        nombreCliente=usuario.first_name+''+usuario.last_name,
        codigoValidacion=CodeFactoryUtil.codigoValidacionEmail(email)).send()
        return validated_data

class CambiarUsuarioValidarCodigoSerializer(serializers.Serializer):
    newusuario = serializers.EmailField()
    codigo = serializers.CharField()   
    user_id =serializers.IntegerField()

    def validate_newusuario(self,newusuario):
        if ( User.objects.filter(username=newusuario).exists()):
            raise serializers.ValidationError({"newusuario":["Correo electronico ya esta registrado"]})
        return newusuario

    def validate(self,data):
        if (CodeFactoryUtil.codigoValidacionEmail(data["newusuario"])!=data["codigo"]):
            raise serializers.ValidationError({"codigo":["El codigo de validacion no corresponde"]})
        return data

    @transaction.atomic
    def create(self, validated_data): 
        usuario = User.objects.get(id=validated_data['user_id'])

        if(usuario.groups.filter(name='prestador').exists()):
            prestador = Prestador.objects.get(user_id=validated_data["user_id"])
            prestador.email = validated_data["newusuario"]
            prestador.user.username =  validated_data["newusuario"]
            prestador.user.email =  validated_data["newusuario"]
            prestador.save()
            prestador.user.save()
        else:
            cliente = Cliente.objects.get(user_id=validated_data["user_id"])
            cliente.email = validated_data["newusuario"]
            cliente.user.username =  validated_data["newusuario"]
            cliente.user.email =  validated_data["newusuario"]
            cliente.save()
            cliente.user.save()
        return validated_data