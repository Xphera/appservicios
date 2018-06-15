from prestadores.models import  (Disponibilidad as Disp,Prestador)
from servicios.models import (CompraDetalleSesion)
import dateparser
from datetime import datetime, date 
import calendar
import json
from django.db.models import Q

class Disponibilidad(object):
    #TODO: revisar parametros de entrada en metodos

    def obtener(self,prestadorId):
        prestador = Prestador.objects.get(pk=prestadorId)
        disponibilidad = Disp.objects.filter(prestador = prestador)
        output={}
        for disp in disponibilidad:
            try:
                output[disp.dia][disp.hora] = disp.disponibilidad
            except Exception as e:
                output[disp.dia]= {}
                output[disp.dia][disp.hora] = disp.disponibilidad   
        return output

    def guardar(self,data):
        bulkDisponibilidad = []
        try: 
            prestador = Prestador.objects.get(pk=1)

            # #buscar y eliminar si prestador tiene disponibilidad registrada.
            Disp.objects.filter(prestador=prestador).delete()

            for diaid, dia in enumerate(data): 
                if( diaid > 0):
                    for horaid,valor in enumerate(dia):
                        disp = Disp()
                        disp.prestador = prestador
                        disp.dia = diaid
                        disp.hora = horaid                        
                        disp.disponibilidad = valor 
                        bulkDisponibilidad.append(disp)             
            Disp.objects.bulk_create(bulkDisponibilidad)
            return True
        except Exception as e:
            return e

    def programacion(self,fechaInicio,prestadorId):
        disponibilidad = self.obtener(prestadorId)
        fechaInicio = dateparser.parse(fechaInicio)

        # obtengo dias pasado y hoy 
        hoy = datetime.now()        
        diaPasado = hoy.date() > fechaInicio.date()
        
        #si diasPasado = true establece disponibidad en false
        if(diaPasado == True):
            dia = fechaInicio.weekday()+1
            for hora in disponibilidad[dia]:
                disponibilidad[dia][hora] = False
        else:    
            esHoy = fechaInicio.date() ==  hoy.date()
            #si es hoy se establece disponibidad en false a las horas pasadas 
            if (esHoy):
                dia = hoy.weekday()+1
                # +2 para llegar a la hora actual mas una hora
                for hora in range(hoy.hour+2):
                    disponibilidad[dia][hora] = False
                  

            sesiones = CompraDetalleSesion.objects.filter(                
                Q(estado_id=2) | Q(estado_id=4),
                # estado_id = 2,
                compraDetalle__estado_id = 1,
                fechaInicio__year=fechaInicio.year,
                fechaInicio__month=fechaInicio.month,
                fechaInicio__day=fechaInicio.day,
                compraDetalle__prestador_id = prestadorId
                )


            for sesion in sesiones:
                dia = sesion.fechaInicio.weekday()+1
                hora = sesion.fechaInicio.hour

                for i in range(0,sesion.compraDetalle.duracionSesion):
                 disponibilidad[dia][hora+i] = False

        return disponibilidad

    def programacionSegunSesion(self,data):
        
        fechaInicio = dateparser.parse(data["fechaInicio"])
        sesion = CompraDetalleSesion.objects.filter(
            Q(estado_id=1) | Q(estado_id=2) | Q(estado_id=4),
            pk=data["sesionId"],
            # estado_id = 1,
            compraDetalle__estado_id = 1
            ).first()

        programacion = self.programacion(data["fechaInicio"],sesion.compraDetalle.prestador.id)

        dia = fechaInicio.weekday()+1
        duracion = sesion.compraDetalle.duracionSesion
 
        for hora in programacion[dia]:
            if(programacion[dia][hora]==True):
                disponible = False
                for i in range(0,duracion):
                    if(programacion[dia][hora+i]==True):
                        disponible = True
                    else:
                        disponible = False
                        break
                if(disponible == False):
                    programacion[dia][hora]=False

        return programacion[dia]
    
    def disponibilidadMesSegunSesion(self,año,mes,sesionId):        
        año= int(año)
        mes=int(mes)        
        ultimodiames = calendar.monthrange(año,mes)[1]
        input={}
        output=[]
        for dia in range(1,ultimodiames+1):
            input['fechaInicio'] = str(date(año,mes,dia))
            input["sesionId"] = sesionId            
            output.append({"dia":datetime(año,mes,dia),"horas":self.programacionSegunSesion(input)})
        return output

    def validarDisponibilidadSegunSesion(self,fechaInicio,sesionId):
        data = {}
        data["fechaInicio"] = str(fechaInicio)
        data["sesionId"] = sesionId
        programacionSegunSesion = self.programacionSegunSesion(data)
        return programacionSegunSesion[fechaInicio.hour]

