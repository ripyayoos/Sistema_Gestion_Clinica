from django.contrib import admin
from .models import Tecnico, Servicio, Diagnostico

admin.site.register(Tecnico)
admin.site.register(Servicio)

class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipo_link', 'tecnico_asignado', 'estado', 'fecha_inicio')
    list_filter = ('estado', 'tecnico_asignado')
    search_fields = ('equipo__num_serie', 'diagnostico_final')
    
    def equipo_link(self, obj):
        return obj.equipo.num_serie 
    equipo_link.short_description = 'Equipo S/N'

admin.site.register(Diagnostico, DiagnosticoAdmin)