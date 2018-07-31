from django.core.management.base import BaseCommand, CommandError
from servicios.models import Servicio
#from utils.Utils.notificacionesAutomaticas.NotificacionesAutomaticasFactory import NotificacionesAutomaticasFactory
from utils.Utils.notificacionesAutomaticas.NotificacionesAutomaticasFactory import NotificacionesAutomaticasFactory

class Command(BaseCommand):

    help = 'Ejecuta la consulta de notificaciones automaticas'

    def add_arguments(self, parser):
        """
        :param parser: 
        :return: 
        parser.add_argument('poll_id', nargs='+', type=int)=int)=int)
        """
        parser.add_argument('notificacion_id', nargs='+', type=str)

    def handle(self, *args, **options):
        """servicios = Servicio.objects.all()
        for servicio in servicios:
            self.stdout.write(self.style.SUCCESS('Servicio: ["%s"]' % servicio))
        """        
        typeNotification = options["notificacion_id"][0] 
        f = NotificacionesAutomaticasFactory()
        f.run(typeNotification)
        

