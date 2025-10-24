from django.db import models

# 1. El Cliente (Relacion 1:N con Equipo)
class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

# 2. El Equipo
class Equipo(models.Model):
    TIPO_CHOICES = [
        ('LAPTOP', 'Laptop'),
        ('DESKTOP', 'Desktop'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=50)
    num_serie = models.CharField(max_length=100, unique=True, verbose_name='Número de Serie')
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='equipos_recibidos')
    
    def __str__(self):
        return f"{self.marca} - S/N: {self.num_serie}"
    
    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"


# 3. El registro de Recepción (Relacion 1:1 con Equipo)
class Recepcion(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, primary_key=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    problema_reportado = models.TextField(verbose_name='Problema Reportado por Cliente')
    
    def __str__(self):
        return f"Recepción {self.equipo.num_serie}"
    
    class Meta:
        verbose_name = "Recepción de Equipo"
        verbose_name_plural = "Registros de Recepción"