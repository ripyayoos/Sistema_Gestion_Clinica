from django.db import models

# 1. Técnico (El estudiante)
class Tecnico(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    
    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"

# 2. Servicio (Para la relación N:M)
class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    costo_estimado = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    
    def __str__(self):
        return self.nombre

# 3. Diagnóstico (El proceso de reparación)
class Diagnostico(models.Model):
    # RELACIÓN 1:N con Equipo (Un equipo puede tener muchos diagnósticos)
    equipo = models.ForeignKey('recepcion.Equipo', on_delete=models.CASCADE, related_name='diagnosticos')
    
    # RELACIÓN 1:N con Técnico (Un técnico realiza muchos diagnósticos)
    tecnico_asignado = models.ForeignKey('Tecnico', on_delete=models.SET_NULL, null=True, related_name='diagnosticos_realizados')
    
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    informe_final = models.TextField(verbose_name='Informe de Diagnóstico')
    
    # RELACIÓN N:M (Un diagnóstico puede tener muchos servicios y viceversa)
    servicios_aplicados = models.ManyToManyField(Servicio, related_name='diagnosticos_que_lo_usan')
    
    ESTADO_CHOICES = [
        ('DIAGNOSTICO', 'En Diagnóstico'),
        ('REPARACION', 'En Reparación'),
        ('LISTO', 'Listo para Entrega'),
        ('ENTREGADO', 'Entregado al Cliente'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DIAGNOSTICO')
    
    def __str__(self):
        return f"Diagnóstico {self.id} - {self.equipo.num_serie}"
    
    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"