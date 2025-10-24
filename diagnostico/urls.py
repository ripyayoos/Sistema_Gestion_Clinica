from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    # HOME
    path('', views.diagnostico_home, name='home'),
    
    # LISTADO (READ)
    path('listado/', views.listado_diagnosticos, name='listado'),
    
    # ASIGNACIÓN / CREACIÓN (CREATE) - Recibe la PK del Equipo a diagnosticar
    path('asignar/<int:equipo_pk>/', views.asignar_diagnostico, name='asignar'),
    
    # DETALLE / ACTUALIZAR (READ/UPDATE) - Recibe la PK del Diagnóstico
    path('detalle/<int:pk>/', views.detalle_diagnostico, name='detalle'),
    
    # ELIMINAR (DELETE)
    path('eliminar/<int:pk>/', views.eliminar_diagnostico, name='eliminar'),
]