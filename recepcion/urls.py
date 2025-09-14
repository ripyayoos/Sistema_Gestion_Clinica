from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registrar, name="registrar_equipo"),
    path("listado/", views.listado, name="listado_equipos"),
    path("detalle/<str:nombre>/", views.detalle, name="detalle_equipo"),
]
