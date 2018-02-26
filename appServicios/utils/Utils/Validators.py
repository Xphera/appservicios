import re
from datetime import datetime, date, timedelta


def es_alfanumerico(valor,espacios = False):
    """
    Calcula si una cadena de caracteres contine unicamente caracteres alfanumericos.
    r"^[A-zñÑáéíóúÁÉÍÓÚ0-9 ]+$"
    :param valor: cadena a evaluar
    :param espacios: (bool) indica si la cadena puede o no contener espacios
    :return: (bool) indicando si la caden cumple o no con la expresion
    """
    expr = r"^[A-zñÑáéíóúÁÉÍÓÚ0-9]+$"
    if(espacios):
        expr = r"^[A-zñÑáéíóúÁÉÍÓÚ0-9 ]+$"
    return re.search(expr, valor) is not None

def menor_que_fecha_actual(fecha):
    """
    Indica si la fecha suministrada es menor que la fecha actual
    :param fecha: fecha a comparar
    :return: (bool)
    """
    fechaActual = datetime.now().date()
    return fecha < fechaActual

def es_numero_telefonico(numero):
    '''
    Indica si un numero telefonico tiene el formato correcto para colombia, soporta fijos y moviles
    6302338
    3188725398
    +576302338
    :param numero: 
    :return: 
    '''
    expr = r"^\(?(\+57)?\)?[- ]?([1-9])?(3[0-9]{2})?[- ]?[1-9][0-9]{2}[- ]?[0-9]{2}[- ]?[0-9]{2}$"
    return re.search(expr, numero) is not None