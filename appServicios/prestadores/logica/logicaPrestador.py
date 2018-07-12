from prestadores.models import  (Prestador)
from prestadores.serializers import (zonaSerializer)
from servicios.models import (CompraDetalleSesion)
from django.contrib.gis.geos import (GEOSGeometry)
from django.db.models import Count
from parametrizacion.serializers import MunicipioSerializer
from django.conf import settings

class LogicaPrestador(object):

    def customSerializer(self,prestador,servicioId):
                response_data = {}
                response_data['id'] = prestador.id
                response_data['nombreCompleto'] = prestador.nombres+' '+prestador.primerApellido+' '+prestador.segundoApellido
                response_data['nombres'] = prestador.nombres
                response_data['primerApellido'] = prestador.primerApellido
                response_data['segundoApellido'] = prestador.segundoApellido
                response_data['tipoDocumento'] = prestador.tipoDocumento
                response_data['numeroDocumento'] = prestador.numeroDocumento
                response_data['telefono'] = prestador.telefono
                response_data['email'] = prestador.email
                response_data['direccion'] = prestador.direccion
                response_data['municipio'] = MunicipioSerializer(prestador.municipio).data
                response_data['fechaNacimiento'] = prestador.fechaNacimiento               
                response_data['perfil'] = prestador.perfil
                response_data['calificacion'] = prestador.calificacion
                response_data['imagePath'] = settings.MEDIA_URL+str(prestador.imagePath)
                response_data['profesion'] = prestador.profesion
                response_data['insignia'] = prestador.insignia

                #paquetes  
                paquetes = []
                if(servicioId==None):
                   objectPaquete =  prestador.prestador_paquetes.all()
                else:
                    objectPaquete =  prestador.prestador_paquetes.filter(paquete__servicio_id = servicioId)

                for pq in  objectPaquete :
                   paquetes.append({
                       'id':pq.paquete.id,
                       'idRelacionPrestadorPaquete':pq.id,
                       'prestadorId': prestador.id,
                       'nombre':pq.paquete.nombre,
                       'detalle':pq.paquete.detalle,
                       'cantidadDeSesiones':pq.paquete.cantidadDeSesiones,
                       'duracionSesion':pq.paquete.duracionSesion,
                       'valor':pq.valor,
                       'servicio':pq.paquete.servicio.nombre,
                   })
                response_data['paquetes'] = paquetes

                #comentarios
                comentarios = []
                cdsQuery = CompraDetalleSesion.objects.filter(
                    compraDetalle__prestador_id = prestador.id,
                    # compraDetalle__estado_id = 1,
                    estado=3,
                   ).exclude(comentario = None).exclude(comentario = "")

                for cds in cdsQuery:
                     comentarios.append({
                       'id':cds.id,
                       'calificacion': cds.calificacion,
                       'paquete': cds.compraDetalle.nombre,
                       'comentario': cds.comentario,
                       'imagePath':  settings.MEDIA_URL+str(cds.compraDetalle.compra.cliente.imagePath),
                       'cliente': cds.compraDetalle.compra.cliente.nombres+' '+cds.compraDetalle.compra.cliente.primerApellido+' '+cds.compraDetalle.compra.cliente.segundoApellido,
                    })
    
                response_data['comentarios'] = comentarios
                    
                #zona
                response_data['zona'] = zonaSerializer(prestador.zona).data
                # formacion
                formacion = []
                for f in prestador.prestador_formacion.all().order_by("-año"):
                    formacion.append({
                       'titulo': f.titulo,
                       'institucion': f.institucion,
                       'year': f.año,
                    })                
                response_data['formacion'] = formacion
                return response_data

    def geolocalizarPrestadorServicio(self,longitud,latitud,servicioId):
        output = []
        pnt = GEOSGeometry('POINT('+str(longitud)+' '+str(latitud)+')')
        queryset=Prestador.objects.filter(
                    zona__zona__intersects=(pnt),
                    prestador_paquetes__paquete__servicio__id = servicioId
                    ).annotate(Count("id")).order_by("-calificacion")

        for q in queryset:
            if(q.zona.zona.intersects(pnt)):        
                output.append(self.customSerializer(q,servicioId))
        return output
  