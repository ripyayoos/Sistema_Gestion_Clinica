from django.urls import path
from . import views

app_name = 'recepcion'

urlpatterns = [
    # Vistas CRUD HTML
    path('', views.recepcion_home, name='home'),
    path('registrar/', views.registrar_equipo, name='registrar'),
    path('listado/', views.listado_equipos, name='listado'),
    path('detalle/<int:pk>/', views.detalle_equipo, name='detalle'),
    path('eliminar/<int:pk>/', views.eliminar_equipo, name='eliminar'), # DELETE HTML

    # API ENDPOINTS (GET, POST, PUT, DELETE)
    path('api/crear/', views.api_crear_recepcion, name='api_crear_recepcion'), # POST
    path('api/detalle/<str:num_serie>/', views.api_detalle_recepcion, name='api_detalle_recepcion'), # GET
    path('api/actualizar/<str:num_serie>/', views.api_actualizar_recepcion, name='api_actualizar_recepcion'), # PUT
    path('api/eliminar/<str:num_serie>/', views.api_eliminar_recepcion, name='api_eliminar_recepcion'), # DELETE
]