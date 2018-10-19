from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from clientes import views
from payU import views  as viewsPayU

urlpatterns = [
 #   path('clientes/', views.cliente_lista),
 #   path('clientes/<int:pk>/', views.cliente_detalle),
 #   path('clientesWraperAnotation/', views.cliente_lista_wrapper_anotation),
 #   path('clientesWraperAnotation/<int:pk>/', views.cliente_detalle_wrapper_anotation),
 #   path('clientesClass/', views.ClienteClassListView.as_view()),
 #  path('clientesClass/<int:pk>/', views.ClienteDetalleClassView.as_view()),
 #  path('clientesMixims/', views.ClienteMiximsList.as_view()),
 #  path('clientesMixims/<int:pk>/', views.ClienteMiximDetalle.as_view()),
 #  path('clientes/', views.ClienteGenericsList.as_view()),
 #  path('clientes/<int:pk>/', views.ClienteGenericsDetalle.as_view()),
    path('registro/', views.RegistroClienteList.as_view()),
    path('validarEmail/', views.ValidarEmailCode.as_view()),
    path('Informacion/', views.Informacion.as_view()),
    path('Informacion/<int:id>/', views.Informacion.as_view()),
    path('Ubicaciones/', views.ClienteUbicaciones.as_view()),
    path('Ubicaciones/<int:id>/', views.ClienteUbicacion.as_view()),
    path('CambiarPassword/', views.CambiarPassword.as_view()),
    path('CambiarUsuario/', views.CambiarUsuario.as_view()),
    path('CambiarUsuarioValidarCodigo/', views.CambiarUsuarioValidarCodigo.as_view()),
    path('TarjetaCredito/', viewsPayU.TarjetaCredito.as_view()),
    path('TarjetaCredito/<uuid:id>/', viewsPayU.TarjetaCredito.as_view()),
    path('Pay/',viewsPayU.Pay.as_view()),
    path('TarjetaCreditoPricipal/',viewsPayU.TarjetaCreditoPricipal.as_view()),
    path('SaldoBolsa/',views.SaldoBolsaViewSet.as_view()),
    path('Bolsa/',views.BolsaViewSet.as_view()),
    path('MisPaquetes/',views.MisPaqueteViewSet.as_view()),
    path('RestablecerPassword/', views.RestablecerPassword.as_view()),
    path('CerrarCuenta/', views.CerrarCuenta.as_view()),
    path('authfb/', views.authfb.as_view()),
    path('authgoog/', views.authgoog.as_view()),
    path('PayConfirmacion/',viewsPayU.PaginaConfirmacion.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

