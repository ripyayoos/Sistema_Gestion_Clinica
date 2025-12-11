from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    # Vistas CRUD HTML
    path('', views.diagnostico_home, name='home'), 
    path('listado/', views.listado_diagnosticos, name='listado'),
    path('asignar/<int:equipo_pk>/', views.asignar_diagnostico, name='asignar'),
    path('detalle/<int:pk>/', views.detalle_diagnostico, name='detalle'),
    path('eliminar/<int:pk>/', views.eliminar_diagnostico, name='eliminar'), # DELETE HTML

    # API ENDPOINTS (GET, PUT, DELETE)
    path('api/detalle/<int:pk>/', views.api_obtener_diagnostico, name='api_obtener'), # GET
    path('api/actualizar/<int:pk>/', views.actualizar_diagnostico, name='api_actualizar'), # PUT
    path('api/eliminar/<int:pk>/', views.api_eliminar_diagnostico, name='api_eliminar'), # DELETE
]