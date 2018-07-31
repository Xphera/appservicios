
import onesignal as onesignal_sdk
from utils.Utils import Utils

class Onesignal(object):
    def __init__(self):
        # self.user_auth_key ="ZDQ4OWYxZGItOTIwMi00NmE5LWI3ZTAtNWI5YzcwZjkwOGQz"
        # self.app_auth_key= "ZTZiZDhmZDMtN2EyZS00MGY4LThhNGQtMGJhZDIwNjM1NDg2"
        # self.app_id = "96150a2e-39ac-477d-a116-16cc8c5e2e88"

         self.keys={
            "prestador":{
                "user_auth_key" : "ZDQ4OWYxZGItOTIwMi00NmE5LWI3ZTAtNWI5YzcwZjkwOGQz",
                "app_auth_key": "ZTZiZDhmZDMtN2EyZS00MGY4LThhNGQtMGJhZDIwNjM1NDg2",
                "app_id" : "96150a2e-39ac-477d-a116-16cc8c5e2e88"
            },
            "cliente":{
               "user_auth_key" : "ZDQ4OWYxZGItOTIwMi00NmE5LWI3ZTAtNWI5YzcwZjkwOGQz",
                "app_auth_key": "YjEwMTBmNWQtYmE4Ny00NmY5LTk4MWMtNTFlYTJlYzMyMTUx",
                "app_id" : "d8540210-8524-4ffe-aaf1-844417fdaf2d"
            },
            "administrador":{
                "user_auth_key" : "ZDQ4OWYxZGItOTIwMi00NmE5LWI3ZTAtNWI5YzcwZjkwOGQz",
                "app_auth_key": "ZTZiZDhmZDMtN2EyZS00MGY4LThhNGQtMGJhZDIwNjM1NDg2",
                "app_id" : "96150a2e-39ac-477d-a116-16cc8c5e2e88"
            }
        }

       
    def onesignalClient(self,a):
        key = self.keys[a]
        
        return onesignal_sdk.Client(
            user_auth_key = key["user_auth_key"], 
            app={"app_auth_key":key["app_auth_key"] , "app_id":key["app_id"] }
            )


    def enviarNotificacion(self,filtro,mensaje,titulo,data,app):
        notificacion = onesignal_sdk.Notification(contents={"en": mensaje})
        notificacion.set_parameter("headings", {"en": titulo})
        notificacion.set_parameter("data",data)
        notificacion.set_filters(filtro)
        onesignal_response =  self.onesignalClient(app).send_notification(notificacion)
        print(onesignal_response.status_code)
        print(onesignal_response.json())

    def fitro(self,userId,app):
        return [
                {"field": "tag", "key": "userId", "relation": "=", "value": userId}, 
  	            {"operator": "AND"},
  	            {"field": "tag", "key": "app", "relation": "=", "value": app}
            ]

    def notificacionSesion(self,sesion,app):
             
        if(sesion.estado_id == 2):
            titulo="Sesión programada"
        elif(sesion.estado_id == 4):
            titulo="Sesión reprogramada"
        elif(sesion.estado_id == 6):
            titulo="Sesión cancelada"  
        elif(sesion.estado_id == 5):
            titulo="Sesión en ejecución" 
        elif(sesion.estado_id == 3):
            titulo="Sesión finalizada"   
 
        if(app=="prestador"):
            userId = sesion.compraDetalle.prestador.user.id
            filtro = self.fitro(userId,"prestador")
            mensaje = sesion.compraDetalle.compra.cliente.nombreCompleto() +" cúando "+ Utils.replaceNone(sesion.fechaInicio) +"  donde "+Utils.replaceNone(sesion.direccion)+" "+Utils.replaceNone(sesion.complemento)    
        elif(app=="cliente"): 
            userId = sesion.compraDetalle.compra.cliente.user.id
            filtro = self.fitro(userId,"cliente")
            mensaje = sesion.compraDetalle.prestador.nombreCompleto() +" cúando "+ Utils.replaceNone(sesion.fechaInicio) +"  donde "+Utils.replaceNone(sesion.direccion)+" "+Utils.replaceNone(sesion.complemento)
            print(sesion,sesion.id)
        else:
            print("algo")
        self.enviarNotificacion(filtro,mensaje,titulo,{'sesionId':sesion.id,'tipo':'detalleSesion'},app)

    def notificacionChat(self,sesionChat,app):
        sesion = sesionChat.compraDetalleSesion
        titulo = "Mensaje Sesión"
        mensaje =  sesionChat.mensaje
        if(app=="prestador"):
            userId = sesion.compraDetalle.prestador.user.id
            filtro = self.fitro(userId,"prestador")
        elif(app=="cliente"): 
            userId = sesion.compraDetalle.compra.user.id 
            filtro = self.fitro(userId,"cliente")
        else:
            print("algo")     

        self.enviarNotificacion(filtro,mensaje,titulo,{'sesionId':sesion.id,'app':'sesionChat','mensaje':mensaje},app)

    def notificacionAutomatica(self,notificaciones):
        for notificacion in notificaciones:
            filtro = self.fitro(notificacion["user_id"],notificacion["app"])
            self.enviarNotificacion(filtro,notificacion["mensaje"],notificacion["titulo"],notificacion["parametros_adicionales"],notificacion["app"])

    