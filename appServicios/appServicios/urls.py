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
from api.views import (UserViewSet)
from clientes.views import (ClienteViewSet,UbicacionViewSet,MediodepagoViewSet)
from prestadores.views import (PrestadorViewSet,)
from parametrizacion.views import (DepartamentoViewSet, MunicipioViewSet, SexoViewSet)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authTokenViews
from rest_framework_swagger.views import get_swagger_view
from servicios.views import (CategoriaViewSet,ServicioViewSet,PaqueteViewSet,CompraViewSet)

router = DefaultRouter()

#PRESTADORES ------------------------------------------------------------------------------------------------
router.register(prefix='prestadores',   viewset=PrestadorViewSet,       base_name='prestador')

#SERVICIOS --------------------------------------------------------------------------------------------------
router.register(prefix='categorias',    viewset=CategoriaViewSet,       base_name='categoria')
router.register(prefix='servicios',     viewset=ServicioViewSet,        base_name='servicio')
router.register(prefix='paquetes',      viewset=PaqueteViewSet,         base_name='paquete')
router.register(prefix='compras',       viewset=CompraViewSet,          base_name='compra')

#CLIENTES ---------------------------------------------------------------------------------------------------
router.register(prefix='clientes',      viewset=ClienteViewSet,         base_name='cliente')
router.register(prefix='ubicaciones',   viewset=UbicacionViewSet,       base_name='ubicacion')
router.register(prefix='mediosDePago',  viewset=MediodepagoViewSet,     base_name='medioDePago')

#PARAMETRICOS -----------------------------------------------------------------------------------------------
router.register(prefix='departamentos', viewset=DepartamentoViewSet,    base_name='departamento')
router.register(prefix='municipios',    viewset=MunicipioViewSet,       base_name='municipio')
router.register(prefix='sexo',          viewset=SexoViewSet,            base_name='sexo')

#API---------------------------------------------------------------------------------------------------------
router.register(prefix='users',viewset=UserViewSet,base_name='user')

#SCHEMA_HELP_VIEW   SWANGGER
schema_view = get_swagger_view(title='APPSERVICIOS XPHERA API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', authTokenViews.obtain_auth_token),
    path('api/clientes/',include('clientes.urls')),
    path('api/parametricos/',include('parametrizacion.urls')),
    path('api/prestadores/',include('prestadores.urls')),
    path('api/servicios/',include('servicios.urls')),
    path('api/nav/',include(router.urls)),
    path('api/help/',schema_view)
]
