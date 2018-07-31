import inflect
from dateutil import relativedelta

def replaceNone(valor):
    return str("") if valor is None else str(valor)
    
def diffTexto(fecha1,fecha2):
    p = inflect.engine()
    difference = relativedelta.relativedelta(fecha1,fecha2)
    if(difference.hours > 0):
        d = str(difference.hours)+" "+p.plural("hora",difference.hours)+" "
    else:
        d = str(difference.minutes)+" "+ p.plural("minuto",difference.minutes)+" "  
    return d