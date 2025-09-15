from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    path('asignar/', views.asignar_tarea, name='asignar'),
    path('evaluar/', views.evaluar_diagnostico, name='evaluar'),
    path('listado/', views.listado_diagnosticos, name='listado'),
]