from django.core.management.base import BaseCommand, CommandError
from parametrizacion.models import (Municipio,Departamento,EstadoSesion,TipoDocumento,Sexo, FranquiciasTarjetasCredito, TipoMedioPago)
from parametrizacion.commonChoices import *

class Command(BaseCommand):


    help = 'Lista todos los servicios registrados'

    def add_arguments(self, parser):
        """
        :param parser: 
        :return: 
        parser.add_argument('poll_id', nargs='+', type=int)=int)=int)
        """

    @transaction.atomic
    def handle(self, *args, **options):

        EstadoSesion.objects.bulk_create([
            EstadoSesion(estado=ESTADO_SESION_POR_INICIAR),
            EstadoSesion(estado=ESTADO_SESION_INICIADA),
            EstadoSesion(estado=ESTADO_SESION_FINALIZADA),
            EstadoSesion(estado=ESTADO_SESION_INTERRUMPIDA),
            EstadoSesion(estado=ESTADO_SESION_AGENDADA),
            EstadoSesion(estado=ESTADO_SESION_CANCELADA)
        ])

        TipoDocumento.objects.bulk_create([
            TipoDocumento(id=CEDULA_CIUDADANIA,tipo="Cédula de Ciudadania"),
            TipoDocumento(id=CEDULA_EXTRANJERIA,tipo="Cédula de Extranjeria"),
            TipoDocumento(id=PASAPORTE,tipo="Pasaaporte"),
            TipoDocumento(id=TARJETA_IDENTIDAD,tipo="Tarjeta de Identidad")
        ])

        Sexo.objects.bulk_create([
            Sexo(id=MASCULINO,sexo="Masculino"),
            Sexo(id=FEMENINO, sexo="Femenino"),
        ])

        FranquiciasTarjetasCredito.objects.bulk_create([
            FranquiciasTarjetasCredito(id=FRANQUICIA_MASTER_CARD,franquicia="MASTER CARD"),
            FranquiciasTarjetasCredito(id=FRANQUICIA_AMERICAN_EXPRESS,franquicia="AMERICAN EXPRESS"),
            FranquiciasTarjetasCredito(id=FRANQUICIA_VISA,franquicia="VISA"),
            FranquiciasTarjetasCredito(id=FRANQUICIA_DINNERS_CLUB,franquicia="DINNERS cCLI")
        ])

        TipoMedioPago.objects.bulk_create([
            TipoMedioPago(id=TARJETA_CREDITO,medioPago="Tarjeta de Credito"),
        ])
