from django.contrib import admin
from .models import Cliente, Equipo, Recepcion

admin.site.register(Cliente)
admin.site.register(Equipo)
admin.site.register(Recepcion)