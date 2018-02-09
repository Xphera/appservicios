from django.conf.urls import url, include

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from servicios.views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'categoria/', CategoriaViewSet)
router.register(r'servicio/', ServicioViewSet)
router.register(r'paquete/', PaqueteViewSet)
router.register(r'compra/', CompraViewSet)


urlpatterns = [
    path('servicios/categoria/',CategoriaViewSet.as_view({'get': 'list','post': 'create'})),
    path('servicios/categoria/<int:pk>/',CategoriaViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'})),
    path('servicios/servicio/', ServicioViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('servicios/servicio/<int:pk>/', ServicioViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)