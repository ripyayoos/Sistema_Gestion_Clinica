from django.urls import path
from . import views

urlpatterns = [
    path('verificar/', views.verificar_equipo, name='verificar'),
    path('reporte/', views.reporte_entrega, name='reporte'),
    path('comprobante/<str:nombre>/', views.comprobante, name='comprobante'),
]
