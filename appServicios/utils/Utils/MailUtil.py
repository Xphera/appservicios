
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
        pass
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


                templatesCurrentPath = settings.BASE_DIR+os.sep+"utils"+os.sep+"Utils"+os.sep+"templatesMails"
                pathHtml = templatesCurrentPath+os.sep+'validacion_registro_cliente.html'
                pathTxt = templatesCurrentPath+os.sep+'validacion_registro_cliente.txt'


                print(pathHtml, pathTxt)

                ##text_content_template = get_template(pathTxt)
                html_content_template = get_template(pathHtml)

                contexto = Context(
                    {
                        'nombreCliente': kwargs["nombreCliente"],
                        'codigoValidacion': kwargs["codigoValidacion"]
                    })

                html_content = render_to_string(pathHtml,{
                        'nombreCliente': kwargs["nombreCliente"],
                        'codigoValidacion': kwargs["codigoValidacion"]
                    })

                text_content = ""#text_content_template.render(contexto)
               # html_content = html_content_template.render(contexto)

                return EmailFactory.makeEmail(
                    subject ='VALIDACION REGISTRO CLIENTE',
                    to = [to],
                    text_content=text_content,
                    html_content= html_content
                )
            elif(email_type is EMAIL_TYPE.VALIDACION_CAMBIO_CORREO):
                pass
            elif(email_type is EMAIL_TYPE.CODIGO_RECUPERACION_CONTRASENA):
                pass
            else:
                raise Exception('El tipo de email no contine una implementación Tipo no encontrado')
        else:
            raise Exception('El tipo de email no corresponde a una instancia valida de EMAIL_TYPE')

    @staticmethod
    def makeEmail(subject,to,text_content,html_content):
        from_email= 'adgranados@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        #msg.send()
        return msg