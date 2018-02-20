"""appServicios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

#from servicios import urls as serviciosUrls
from rest_framework.routers import DefaultRouter
from servicios.views import (CategoriaViewSet,ServicioViewSet,PaqueteViewSet,CompraViewSet)
from clientes.views import (ClienteViewSet,UbicacionViewSet,MediodepagoViewSet)
from prestadores.views import (PrestadorViewSet,)
from parametrizacion.views import (DepartamentoViewSet, MunicipioViewSet)
from api.views import (UserViewSet)
router = DefaultRouter()

#PRESTADORES
router.register('prestadores',PrestadorViewSet, 'prestador')
#SERVICIOS
router.register('categorias', CategoriaViewSet, 'categoria')
router.register('servicios', ServicioViewSet, 'servicio')
router.register('paquetes', PaqueteViewSet, 'paquete')
router.register('compras', CompraViewSet, 'compra')
#CLIENTES
router.register('clientes', ClienteViewSet, 'cliente')
router.register('ubicaciones', UbicacionViewSet, 'ubicacion')
router.register('mediosDePago', MediodepagoViewSet, 'medioDePago')

#PARAMETRICOS
router.register('departamentos',DepartamentoViewSet, 'departamento')
router.register('municipios',MunicipioViewSet, 'municipio')
#API
router.register('users',UserViewSet,'user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/clientes/',include('clientes.urls')),
    path('api/nav/',include(router.urls))
]
