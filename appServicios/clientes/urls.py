from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from clientes import views

urlpatterns = [
    path('clientes/', views.cliente_lista),
    path('clientes/<int:pk>/', views.cliente_detalle),
    path('clientesWraperAnotation/', views.cliente_lista_wrapper_anotation),
    path('clientesWraperAnotation/<int:pk>/', views.cliente_detalle_wrapper_anotation),
    path('clientesClass/', views.ClienteClassListView.as_view()),
    path('clientesClass/<int:pk>/', views.ClienteDetalleClassView.as_view()),
    path('clientesMixims/', views.ClienteMiximsList.as_view()),
    path('clientesMixims/<int:pk>/', views.ClienteMiximDetalle.as_view()),
    path('clientesGenerics/', views.ClienteGenericsList.as_view()),
    path('clientesGenerics/<int:pk>/', views.ClienteGenericsDetalle.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

