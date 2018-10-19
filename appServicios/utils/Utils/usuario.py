from rest_framework import serializers
from rest_framework.authtoken.models import Token 
from utils.Utils.CodigosUtil import CodeFactoryUtil
from utils.Utils import Validators
from utils.Utils.MailUtil import EMAIL_TYPE, EmailFactory
from django.db import DatabaseError, transaction, IntegrityError
from django.contrib.auth.models import User,Group
from clientes.models import (Cliente)
from prestadores.models import (Prestador)
from random import random

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
            return self.infoToken(request.user)
            # Token.objects.get(user=request.user).delete()
            # token = Token.objects.create(user=request.user)
            # output["estado"]=True
            # output["token"]=token.key
            # return output
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
            return self.infoToken(request.user)
            # Token.objects.get(user=request.user).delete()
            # token = Token.objects.create(user=request.user)
            # output["estado"]=True
            # output["token"]=token.key
            # return output
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
            user = User.objects.get(username=serializer.data.get("usuario"))
            user.set_password(serializer.data.get("password"))
            user.save()
            return self.infoToken(user)
            # Token.objects.get(user=user).delete()
            # token = Token.objects.create(user=user)
            
            # if(user.groups.filter(name='cliente').exists()):
            #     c = Cliente.objects.get(user=user)
            #     fullname=str(c.nombres)+' '+str(c.primerApellido)+' '+str(c.segundoApellido)
            # elif(user.groups.filter(name='administrador').exists()):
            #     print('administrador')
            # else:
            #     p = Prestador.objects.get(user=user)
            #     fullname=p.nombres+' '+p.primerApellido+' '+p.segundoApellido
            # output["estado"]=True
            # output["token"]=token.key
            # output["user_id"]=user.pk
            # output["email"]=user.email
            # output["fullname"]=fullname
            # return output       
        else:
            output["estado"]=False
            output["error"]=serializer.errors
            return output

    def infoToken(self,user):
        output={}
        try:
            Token.objects.get(user=user).delete()
        except Exception as e:
            print(e)
        
        token = Token.objects.create(user=user)
            
        if(user.groups.filter(name='cliente').exists()):
            c = Cliente.objects.get(user=user)
            fullname= c.nombreCompleto()
            imagen = c.obtenerImagePath()
        elif(user.groups.filter(name='administrador').exists()):
            print('administrador')
        else:
            p = Prestador.objects.get(user=user)
            fullname=p.nombreCompleto()
            imagen = str(p.imagePath)

        output["estado"]=True
        output["token"]=token.key
        output["user_id"]=user.pk
        output["email"]=user.email
        output["fullname"]=fullname
        output["imagen"]=imagen
        return output       

    def cerrarCuenta(self,user):
        try:                           
            # acciones cliente_cliente    
            # cerrarCuenta = True
            # activo = false
            rand = str(random())
            if(user.groups.filter(name='cliente').exists()):
                c = Cliente.objects.get(user=user)
                c.cuentaCerrada = True
                c.email = "cuentaCerrada-"+rand+"-"+c.email
                c.activo = False
                c.save()
            # acciones en auth_user:
            # username = eliminado
            # email= vacio
            # is_activate = 0
            user.username = "cuentaCerrada-"+rand+"-"+user.username
            user.email = "" 
            user.is_active=False
            user.save()

            # token:
            # limpiar token
            Token.objects.get(user=user).delete()
            return True
        except Exception as e:
            print(e,user)
            return False

    def registroUsuario(self,email,passw):
        user = User.objects.create_user(email, password=passw)
        user.is_superuser = False
        user.is_staff = False
        user.email = email
        user.save()
        group = Group.objects.get(name='cliente')
        group.user_set.add(user)

        cliente = Cliente()
        cliente.email = user.email
        cliente.user_id = user.id
        cliente.save()
        return cliente


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
            raise serializers.ValidationError("Usuario ya registrado")
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