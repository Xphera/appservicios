from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from prestadores import views

urlpatterns = [
    path('Disponibilidad/', views.DisponibilidadViewSet.as_view()),
    path('programacionSegunSesion/', views.programacionSegunSesionViewSet.as_view()),
    path('disponibilidadMesSegunSesion/', views.disponibilidadMesSegunSesion.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
