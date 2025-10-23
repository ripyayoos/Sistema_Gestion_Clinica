from django.urls import path
from . import views

app_name = 'entrega'

urlpatterns = [
    path('', views.entrega_home, name='home'),
    path('verificar/', views.verificar_equipo, name='verificar'),
    path('confirmar/<int:pk>/', views.confirmar_entrega, name='confirmar'), 
    path('reporte/<int:pk>/', views.reporte_entrega, name='reporte'),
]