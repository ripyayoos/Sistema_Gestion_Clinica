from django import forms
from .models import Cliente, Equipo, Recepcion

# Formulario para el Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'email', 'telefono'] 
        labels = {
            'rut': 'RUT del Cliente',
            'email': 'Email',
        }
        
# Formulario para el Equipo
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        exclude = ['cliente'] 
        labels = {
            'tipo': 'Tipo de Equipo',
            'marca': 'Marca',
            'num_serie': 'Número de Serie',
        }

# Formulario para el Registro de Recepción 
class RecepcionForm(forms.ModelForm):
    class Meta:
        model = Recepcion
        exclude = ['equipo', 'fecha_ingreso'] 
        labels = {
            'problema_reportado': 'Problema Reportado por Cliente',
        }