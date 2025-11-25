from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    path('', views.diagnostico_home, name='home'),
    path('listado/', views.listado_diagnosticos, name='listado'),
    path('asignar/<int:equipo_pk>/', views.asignar_diagnostico, name='asignar'),
    path('detalle/<int:pk>/', views.detalle_diagnostico, name='detalle'),
    path('eliminar/<int:pk>/', views.eliminar_diagnostico, name='eliminar'),

    #API ENDPOINT
    path('api/crear/', views.crear_diagnostico, name='crear'),
    path('api/actualizar/<int:pk>/', views.actualizar_diagnostico, name='actualizar'),
]