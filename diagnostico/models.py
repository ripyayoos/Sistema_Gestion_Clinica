from django.db import models
# Usamos cadena de texto para la importación por seguridad de carga
from recepcion.models import Equipo 

# 1. Técnico (Relación 1:N con Diagnóstico)
class Tecnico(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"

# 2. Servicio (Relación N:M con Diagnóstico)
class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    costo_estimado = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    
    def __str__(self):
        return self.nombre

# 3. Diagnóstico
class Diagnostico(models.Model):
    
    ESTADO_CHOICES = [
        ('DIAGNOSTICO', 'En Diagnóstico'),
        ('REPARACION', 'En Reparación'),
        ('LISTO', 'Listo para Entrega'),
        ('ENTREGADO', 'Entregado al Cliente'), 
    ]
    
    # RELACIÓN 1:N con Equipo (Usando cadena de texto para evitar problemas de importación)
    equipo = models.ForeignKey('recepcion.Equipo', on_delete=models.CASCADE, related_name='diagnosticos')
    
    # RELACIÓN 1:N con Técnico
    tecnico_asignado = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, related_name='diagnosticos_realizados')
    
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    informe_final = models.TextField(verbose_name='Informe de Diagnóstico y Solución')
    
    # RELACIÓN N:M 
    servicios_aplicados = models.ManyToManyField(Servicio, related_name='diagnosticos_que_lo_usan')
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DIAGNOSTICO')
    
    def __str__(self):
        return f"Diagnóstico {self.id} - {self.equipo.num_serie}"
    
    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"