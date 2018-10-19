import facebook
from utils.Utils.usuario import Usuario
from clientes.models import (Cliente)
from django.contrib.auth.models import User,Group
import datetime
from urllib import request
from django.conf import settings
from parametrizacion.models import Sexo
from utils.Utils.google import Google

class loginSocial(object):
    getDataSocial = {}
    def __init__(self):
        self.getDataSocial = {
            'id':'',
            'name':'',
            'gender':'',
            'birthday':'', 
            'picture':'',
        }
    def loginGoogle(self,token,userId):  
        usuario = Usuario()
        googleApi = Google(token=token,userId=userId)
        try:
            # buscar usuario por de facebook
            usuarioGoogle =  googleApi.request('https://www.googleapis.com/plus/v1/people/')           
            try:            
                cliente = Cliente.objects.get(idGoog=usuarioGoogle["id"])
                output = output={"error":False,"mensaje":usuario.infoToken(cliente.user)} 
            except Cliente.DoesNotExist:
                try:     
                    gender=None
                    if('gender' in usuarioGoogle):
                        if( usuarioGoogle["gender"] == 'male'):
                            gender= Sexo.objects.get(id='M')
                        elif( usuarioGoogle["gender"] == 'female'):
                            gender=Sexo.objects.get(id='F')

                    self.getDataSocial["email"]=usuarioGoogle["emails"][0]["value"]   

                    self.getDataSocial["id"]= usuarioGoogle["id"] if 'id' in usuarioGoogle else None
                    self.getDataSocial["name"] = usuarioGoogle["displayName"] if 'displayName' in usuarioGoogle else ''       
                    self.getDataSocial["birthday"]=  datetime.datetime.strptime(usuarioGoogle["birthday"],'%Y-%m-%d') if 'birthday' in usuarioGoogle else None
                    self.getDataSocial["gender"]=  gender    
                    self.getDataSocial["picture"] = usuarioGoogle["image"]["url"] if 'image' in usuarioGoogle else None

                    u = self.crearUsuario()
                    u.idGoog = self.getDataSocial["id"]        
                    u.save()
                                
                    output = output={"error":False,"mensaje":usuario.infoToken(u.user)}               

                except Exception as e:
                    print(e)
                    output={"error":True,"mensaje": 'No se tuvo acceso a email'}
        except Exception as e:
            print(e)
            output={"error":True,"mensaje":"Error a validar token de google "}

        return output

    def loginFB(self,token):
   
        graph = facebook.GraphAPI(access_token=token, version="3.0")
        usuario = Usuario()
        output = {}
        try:
            usuariofb =  graph.request('/me?fields=email,id,name,gender,birthday,picture')
            try:
            # buscar usuario por de facebook
                cliente = Cliente.objects.get(idFb=usuariofb["id"])
                output = output={"error":False,"mensaje":usuario.infoToken(cliente.user)} 
            except Cliente.DoesNotExist:    
                try: 
                    #tipo de genero
                    gender=None
                    if('gender' in usuariofb):
                        if( usuariofb["gender"] == 'male'):
                            gender= Sexo.objects.get(id='M')
                        elif( usuariofb["gender"] == 'female'):
                             gender=Sexo.objects.get(id='F')

                    self.getDataSocial["email"]=usuariofb["email"]         
                    self.getDataSocial["id"]= usuariofb["id"] if 'id' in usuariofb else None
                    self.getDataSocial["name"] = usuariofb["name"] if 'name' in usuariofb else ''       
                    self.getDataSocial["birthday"]= datetime.datetime.strptime(usuariofb["birthday"],'%m/%d/%Y') if 'birthday' in usuariofb else None
                    self.getDataSocial["gender"]=  gender    
                    self.getDataSocial["picture"] = usuariofb["picture"]["data"]["url"] if 'picture' in usuariofb else None
                    
                    u = self.crearUsuario()
                    u.idFb = self.getDataSocial["id"]
                    u.save()
                    
                    output = output={"error":False,"mensaje":usuario.infoToken(u.user)} 
                except Exception as e:
                    print(e)
                    output={"error":True,"mensaje": 'No se tuvo acceso a email'}
        except Exception as e:
            print(e)
            output={"error":True,"mensaje":"Error a validar Token de facebook "}
        return output

    def crearUsuario(self):
        # usuario = Usuario()
        try:
            cliente = Cliente.objects.get(email=self.getDataSocial["email"],cuentaCerrada=0)            
        except Cliente.DoesNotExist:
            # obtiene nombre de app
            appName = __package__.rsplit('.', 1)[0]
            #crear usuario    
            cliente =  Usuario().registroUsuario(self.getDataSocial["email"],self.getDataSocial["id"])       
            
            cliente.activo=True
            cliente.nombres = self.getDataSocial["name"]
            cliente.fechaNacimiento = self.getDataSocial["birthday"]            
            cliente.sexo = self.getDataSocial["gender"]  
            if(self.getDataSocial["picture"] != None):
                cliente.imagePath.name =  appName+"/"+str(cliente.id)+".jpg"                                      
                request.urlretrieve(self.getDataSocial["picture"] , settings.MEDIA_ROOT+str(cliente.imagePath.name))
            cliente.save()
        return cliente