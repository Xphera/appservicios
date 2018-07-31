from utils.Utils.notificacionesAutomaticas.INotificacion import INotificacion, NotificacionObject
from utils.Utils.notificacionesAutomaticas.logica.sesion import sesion
from utils.Utils.onesignal import Onesignal

NOTIFICACION_PROXIMAS_SESIONES = "NOTIFICACION_PROXIMAS_SESIONES"
NOTIFICACION_SESIONES_NO_INICIADA = "NOTIFICACION_SESIONES_NO_INICIADA"

class NotificarSesiones(INotificacion):
    def proximaSesiones(self):
        #consultar y armar los objetos        
        s=sesion()
        sesiones = s.proximasesiones()
        return sesiones["prestador"]+sesiones["cliente"]
    def sesionesNoIniciada(self):
        #consultar y armar los objetos        
        s=sesion()
        sesiones = s.sesionesNoIniciada()
        return sesiones

class NotificacionesAutomaticasFactory:

    def __init__(self, *args, **kwargs):
        self.notificaciones = []
        self.os = Onesignal()
        
    def enviarNotificaciones(self):
        self.os.notificacionAutomatica(self.notificaciones)
        
    def run(self,notificacionType):        
        if(notificacionType == NOTIFICACION_PROXIMAS_SESIONES):
            n = NotificarSesiones()
            self.notificaciones = n.proximaSesiones()
        elif(notificacionType is not NOTIFICACION_SESIONES_NO_INICIADA):
            n = NotificarSesiones()
            self.notificaciones=n.sesionesNoIniciada()
        self.enviarNotificaciones()
            