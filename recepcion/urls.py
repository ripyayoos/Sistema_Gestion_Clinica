from django.urls import path
from . import views

app_name = 'recepcion'

urlpatterns = [
    # HOME
    path('', views.recepcion_home, name='home'), 
    
    # CRUD - CREATE/LEER
    path('registrar/', views.registrar_equipo, name='registrar'),
    path('listado/', views.listado_equipos, name='listado'),
    
    # CRUD - LEER/ACTUALIZAR/ELIMINAR - Usamos <int:pk> (Primary Key) en lugar de <str:nombre>
    path('detalle/<int:pk>/', views.detalle_equipo, name='detalle'),
    path('eliminar/<int:pk>/', views.eliminar_equipo, name='eliminar'), # Nueva ruta DELETE
]