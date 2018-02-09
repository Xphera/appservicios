from django.core.management.base import BaseCommand, CommandError
from servicios.models import Servicio

class Command(BaseCommand):


    help = 'Lista todos los servicios registrados'

    def add_arguments(self, parser):
        """
        :param parser: 
        :return: 
        parser.add_argument('poll_id', nargs='+', type=int)=int)=int)
        """

    def handle(self, *args, **options):
        servicios = Servicio.objects.all()
        for servicio in servicios:
            self.stdout.write(self.style.SUCCESS('Servicio: ["%s"]' % servicio))