from django.urls import path
from . import views

app_name = 'entrega'

urlpatterns = [
    # HOME (Lista de equipos listos para entrega)
    path('', views.entrega_home, name='home'),
    
    # BUSCAR EQUIPO POR S/N O RUT (Search)
    path('verificar/', views.verificar_equipo, name='verificar'),
    
    # CONFIRMAR ENTREGA (UPDATE/DELETE) - Usa la PK del Diagnóstico
    path('confirmar/<int:pk>/', views.confirmar_entrega, name='confirmar'), 
    
    # REPORTE/COMPROBANTE (READ) - Usa la PK del Diagnóstico
    path('reporte/<int:pk>/', views.reporte_entrega, name='reporte'),
]