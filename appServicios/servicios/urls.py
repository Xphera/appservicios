from django.conf.urls import url, include

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


from servicios.views import *

# Create a router and register our viewsets with it.

"""path('servicios/categoria/',CategoriaViewSet.as_view({'get': 'list','post': 'create'})),
   path('servicios/categoria/<int:pk>/',CategoriaViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'})),
   path('servicios/servicio/', ServicioViewSet.as_view({'get': 'list', 'post': 'create'})),
   path('servicios/servicio/<int:pk>/', ServicioViewSet.as_view(
       {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
"""
router = DefaultRouter()

router.register('categorias', CategoriaViewSet, 'categoria')
router.register('servicios', ServicioViewSet, 'servicio')
router.register('paquetes', PaqueteViewSet, 'paquete')
router.register('compras', CompraViewSet, 'compra')
# router.register('CalificarSesion', CalificarSesionViewSet, 'compradetalle')
# router.register('PaqueteActivo', PaqueteActivoViewSet,'PaqueteActivo')
# router.register('ProximaSesion', ProximaSesionViewSet,'ProximaSesion')


urlpatterns = [
    path('base/',include(router.urls)),
    path('CalificarSesion/', CalificarSesionViewSet.as_view()),
    path('PaqueteActivo/', PaqueteActivoViewSet.as_view()),
    path('ProximaSesion/', ProximaSesionViewSet.as_view()),
    path('ProgramarSesion/', ProgramarSesionViewSet.as_view()),
    path('Zona/', ZonaSesionViewSet.as_view()),
    path('Zona/<int:pk>/', ZonaSesionViewSet.as_view()),
    path('IniciarSesion/', IniciarSesionViewSet.as_view()),
    path('FinalizarSesion/', FinalizarSesionViewSet.as_view()),
    path('CancelarSesion/', CancelarSesionViewSet.as_view()),
    path('CancelarPaquete/', CancelarPaqueteViewSet.as_view()),
    path('RenovarPaquete/', RenovarPaqueteViewSet.as_view()),
    path('SesionChat/<int:pk>/', SesionChat.as_view()),
    
]

#urlpatterns = format_suffix_patterns(urlpatterns)