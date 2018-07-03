from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from prestadores import views

urlpatterns = [
    path('Disponibilidad/', views.DisponibilidadViewSet.as_view()),
    # path('programacionSegunSesion/', views.programacionSegunSesionViewSet.as_view()),    
    # path('Zona/<int:pk>/', views.zonaViewSet.as_view()),
    path('disponibilidadMesSegunSesion/', views.disponibilidadMesSegunSesionViewSet.as_view()),
    path('Zona/', views.zonaViewSet.as_view()),
    path('SesionPorIniciar/', views.SesionPorIniciarViewSet.as_view()),
    path('SesionProxima/', views.SesionProximaViewSet.as_view()),
    path('SesionFinalizada/', views.SesionFinalizadaViewSet.as_view()),
    path('SesionIniciada/', views.SesionIniciadaViewSet.as_view()),
    # path('Prestador/', views.PrestadorViewSet.as_view()),
    # path('Prestadores/', views.PrestadoresViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
