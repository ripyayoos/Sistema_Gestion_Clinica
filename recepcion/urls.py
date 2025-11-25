from django.urls import path
from . import views

app_name = 'recepcion'

urlpatterns = [
    path('', views.recepcion_home, name='home'), 
    path('registrar/', views.registrar_equipo, name='registrar'),
    path('listado/', views.listado_equipos, name='listado'),
    path('detalle/<int:pk>/', views.detalle_equipo, name='detalle'),
    path('eliminar/<int:pk>/', views.eliminar_equipo, name='eliminar'),

    # API endpoints
    path('api/recepcion/', views.api_crear_recepcion, name="api_crear_recepcion"),
    path('api/recepcion/<str:num_serie>/', views.api_actualizar_recepcion, name="api_actualizar_recepcion"),

]