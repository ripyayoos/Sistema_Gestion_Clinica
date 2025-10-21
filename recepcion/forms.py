
from django import forms
from .models import Cliente, Equipo, Recepcion

# Formulario para el Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Excluye 'id' si no lo tienes en el modelo Cliente
        fields = ['rut', 'nombre', 'apellido', 'email', 'telefono'] 
        labels = {
            'rut': 'RUT del Cliente',
            'email': 'Email',
        }
        
# Formulario para el Equipo
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        # Excluye 'cliente' porque se añade automáticamente en la vista
        exclude = ['cliente'] 
        labels = {
            'tipo': 'Tipo de Equipo',
            'marca': 'Marca',
            'num_serie': 'Número de Serie',
        }

# Formulario para el Registro de Recepción (Problema reportado)
class RecepcionForm(forms.ModelForm):
    class Meta:
        model = Recepcion
        # Excluye 'equipo' y 'fecha_ingreso' (auto_now_add)
        exclude = ['equipo', 'fecha_ingreso'] 
        labels = {
            'problema_reportado': 'Problema Reportado por Cliente',
        }