
from enum import Enum, auto as enum_auto
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.template import Context
from appServicios import settings
import os


class EMAIL_TYPE(Enum):
    VALIDACION_REGISTRO_CLIENTE = enum_auto()
    VALIDACION_CAMBIO_CORREO = enum_auto()
    CODIGO_RECUPERACION_CONTRASENA = enum_auto()


class EmailFactory():
    def __init__(self):
        raise Exception("Esta clase no se debe instanciar");


    @staticmethod
    def getInstance(email_type,to,**kwargs):
        if(type(email_type) is EMAIL_TYPE ):
            if(email_type is EMAIL_TYPE.VALIDACION_REGISTRO_CLIENTE):
                if ("nombreCliente" not in kwargs):
                    raise Exception(
                        "Falto el argumento nombreCliente para enviar el Email de VALIDACION_REGISTRO_CLIENTE");
                if ("codigoValidacion" not in kwargs):
                    raise Exception(
                        "Falto el argumento codigoValidacion para enviar el Email de VALIDACION_REGISTRO_CLIENTE");

                EmailFactory.makeEmailValidacionRegistroCliente(to,**kwargs)
            elif(email_type is EMAIL_TYPE.VALIDACION_CAMBIO_CORREO):
                pass
            elif(email_type is EMAIL_TYPE.CODIGO_RECUPERACION_CONTRASENA):
                pass
            else:
                raise Exception('El tipo de email no contine una implementación Tipo no encontrado')
        else:
            raise Exception('El tipo de email no corresponde a una instancia valida de EMAIL_TYPE')

    @staticmethod
    def getFullPathsMailTemplates(templateHtml, templateTxt):
        """
        Obtiene el path completo para los templates de html y txt suministrados
        :param templateHtml: nombre del archivo template .html 
        :param templateTxt:  nombre del archivo template .txt
        :return: Tupla que contiene las rutas completas de los 2 archivos (pathHtml,pathTxt)
        """
        templatesCurrentPath = settings.BASE_DIR + os.sep + "utils" + os.sep + "Utils" + os.sep + "templatesMails"
        pathHtml = templatesCurrentPath + os.sep + templateHtml
        pathTxt = templatesCurrentPath + os.sep + templateTxt

        return (pathHtml, pathTxt)

    @staticmethod
    def renderTemplates(templateHtml,templateTxt,contexto):
        (pathHtml,pathTxt) = EmailFactory.getFullPathsMailTemplates( templateHtml, templateTxt)
        return (render_to_string(pathHtml, contexto), render_to_string(pathTxt , contexto))

    @staticmethod
    def makeEmailValidacionRegistroCliente(to,nombreCliente,codigoValidacion):
        """
        Construye un Objeto de tipo EmailFactory.makeEmail, listo para enviar
        :param to: Destinatario del correo
        :param nombreCliente: Nombre del cliente/correo electronico
        :param codigoValidacion:  codigo de validacion calculado
        :return: EmailFactory.makeEmail
        """

        contexto = {
            'nombreCliente': nombreCliente,
            'codigoValidacion': codigoValidacion
        }

        (html_content, text_content) =  EmailFactory.renderTemplates(
            templateHtml='validacion_registro_cliente.html',
            templateTxt='validacion_registro_cliente.txt',
            contexto=contexto
        )

        return EmailFactory.makeEmail(
                subject='VALIDACION REGISTRO CLIENTE',
                to=[to],
                text_content=text_content,
                html_content=html_content
            )


    @staticmethod
    def makeEmail(subject,to,text_content,html_content):
        from_email= 'adgranados@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        #msg.send()
        return msg