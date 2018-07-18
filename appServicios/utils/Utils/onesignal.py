
import onesignal as onesignal_sdk
from utils.Utils import Utils

class Onesignal(object):
    def __init__(self):
        self.user_auth_key = "ZDQ4OWYxZGItOTIwMi00NmE5LWI3ZTAtNWI5YzcwZjkwOGQz"
        self.app_auth_key= "ZTZiZDhmZDMtN2EyZS00MGY4LThhNGQtMGJhZDIwNjM1NDg2"
        self.app_id = "96150a2e-39ac-477d-a116-16cc8c5e2e88"

        self.onesignal_client = onesignal_sdk.Client(user_auth_key= self.user_auth_key, 
        app={"app_auth_key":self.app_auth_key , "app_id":self.app_id })

    def enviarNotificacion(self,filtro,mensaje,titulo,data):
        notificacion = onesignal_sdk.Notification(contents={"en": mensaje})
        notificacion.set_parameter("headings", {"en": titulo})
        notificacion.set_parameter("data",data)
        notificacion.set_filters(filtro)
        onesignal_response =  self.onesignal_client.send_notification(notificacion)
        print(onesignal_response.status_code)
        print(onesignal_response.json())

    def fitro(self,userId,tipo):
        return [
                {"field": "tag", "key": "userId", "relation": "=", "value": userId}, 
  	            {"operator": "AND"},
  	            {"field": "tag", "key": "tipo", "relation": "=", "value": tipo}
            ]

    def notificacionSesion(self,sesion,tipo):        
        if(sesion.estado_id == 2):
            titulo="Sesión programada"
        elif(sesion.estado_id == 4):
            titulo="Sesión reprogramada"
        elif(sesion.estado_id == 6):
            titulo="Sesión cancelada"    
 
        if(tipo=="prestador"):
            userId = sesion.compraDetalle.prestador.user.id
            filtro = self.fitro(userId,"prestador")
            mensaje = "Cliente "+ sesion.compraDetalle.compra.cliente.nombreCompleto() +" cúando "+ Utils.replaceNone(sesion.fechaInicio) +"  donde "+Utils.replaceNone(sesion.direccion)+" "+Utils.replaceNone(sesion.complemento)    
        elif(tipo=="cliente"): 
            userId = sesion.compraDetalle.compra.user.id 
        else:
            print("algo")

        self.enviarNotificacion(filtro,mensaje,titulo,{'sesionId':sesion.id,'tipo':'detalleSesion'})


