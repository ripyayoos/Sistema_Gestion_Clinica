from django.shortcuts import render, redirect
from django.contrib import messages
from recepcion.views import EQUIPOS
from diagnostico.views import DIAGNOSTICOS
from Proyecto_Clinica.utils import login_required_session

# Create your views here.
@login_required_session
def verificar_equipo(request):
    nombre = request.GET.get('nombre')
    equipo = next((e for e in EQUIPOS if e['nombre'] == nombre), None) if nombre else None
    return render(request, 'entrega/verificar.html', {'equipo': equipo})

@login_required_session
def reporte_entrega(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones')
        equipo = next((e for e in EQUIPOS if e['nombre'] == nombre), None)
        if not equipo:
            messages.error(request, 'Equipo no encontrado.')
            return redirect('verificar')
        equipo['estado'] = estado
        equipo['observaciones'] = observaciones
        messages.success(request, 'Estado de entrega actualizado.')
        return redirect('comprobante', nombre=nombre)
    return redirect('verificar')

@login_required_session
def comprobante(request, nombre):
    equipo = next((e for e in EQUIPOS if e['nombre'] == nombre), None)
    diagnostico = next((d for d in DIAGNOSTICOS if d['equipo'] == nombre), None)
    if not equipo:
        messages.error(request, 'Equipo no encontrado.')
        return redirect('verificar')
    return render(request, 'entrega/comprobante.html', {'equipo': equipo, 'diagnostico': diagnostico})
