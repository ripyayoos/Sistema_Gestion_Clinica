from django import forms
from .models import Diagnostico, Tecnico, Servicio
from recepcion.models import Equipo

class DiagnosticoForm(forms.ModelForm):

    class Meta:
        model = Diagnostico
        exclude = ['equipo'] 
        widgets = {
            'informe_final': forms.Textarea(attrs={'rows': 4}),
            'servicios_aplicados': forms.CheckboxSelectMultiple, 
        }
        labels = {
            'tecnico_asignado': 'Técnico Asignado',
            'informe_final': 'Informe de Diagnóstico y Solución',
            'servicios_aplicados': 'Servicios Realizados',
            'estado': 'Estado Actual del Diagnóstico',
        }