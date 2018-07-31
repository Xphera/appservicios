from abc import ABCMeta, abstractmethod

class NotificacionObject:
    
    def __init__(self, *args, **kwargs):

        """
        Este campo permite 3 valores:
        cliente, prestador, administrador
        """
        self.app =""
        self.user_id = 0
        self.sesion_id = 0
        """ 
        ---------------------------------- 
        Informacion de la notificacion.
        ---------------------------------- 
        """
        self.titulo = ""
        self.subtitulo = ""
        self.mensaje = ""
        self.parametros_adicionales = {}
        self.urlImage = ""
        self.urlIcon = ""

class INotificacion:
    __metaclass__ = ABCMeta

    """
    Este metodo debe retornar un listado de objetos NotificacionObject.
    """
    @abstractmethod
    def makeNotifications(self, *args, **kwargs): raise NotImplementedError