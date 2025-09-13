from django.urls import path
from . import views

urlpatterns = [
    path('asignar/', views.asignar_tarea, name='asignar'),
    path('evaluar/', views.evaluar_diagnostico, name='evaluar'),
    path('listado/', views.listado_diagnosticos, name='listado_diagnosticos'),
]
