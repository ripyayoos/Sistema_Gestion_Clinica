from django import forms
from .models import Diagnostico, Tecnico, Servicio
from recepcion.models import Equipo

class DiagnosticoForm(forms.ModelForm):
    # Definimos el campo 'equipo' aquí, pero lo haremos Hidden en la vista
    # equipo = forms.ModelChoiceField(queryset=Equipo.objects.all(), label="Equipo a Diagnosticar")

    class Meta:
        model = Diagnostico
        # Excluimos 'equipo' porque se lo pasamos en la vista
        exclude = ['equipo'] 
        widgets = {
            'informe_final': forms.Textarea(attrs={'rows': 4}),
            'servicios_aplicados': forms.CheckboxSelectMultiple, # Para la relación N:M
        }
        labels = {
            'tecnico_asignado': 'Técnico Asignado',
            'informe_final': 'Informe de Diagnóstico y Solución',
            'servicios_aplicados': 'Servicios Realizados',
            'estado': 'Estado Actual del Diagnóstico',
        }