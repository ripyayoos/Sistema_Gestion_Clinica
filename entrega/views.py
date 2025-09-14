from django.shortcuts import render, redirect
from django.contrib import messages
from recepcion.views import equipos_registrados
from diagnostico.views import DIAGNOSTICOS

def verificar_equipo(request):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    nombre = request.GET.get('nombre')
    equipo = next((e for e in equipos_registrados if e['cliente'] == nombre), None) if nombre else None
    return render(request, 'entrega/verificar.html', {'equipo': equipo})

def reporte_entrega(request):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones')
        
        equipo = next((e for e in equipos_registrados if e['cliente'] == nombre), None)
        if not equipo:
            messages.error(request, 'Equipo no encontrado.')
            return redirect('/entrega/verificar/')
        
        equipo['estado'] = estado
        equipo['observaciones'] = observaciones
        messages.success(request, 'Estado de entrega actualizado.')
        return redirect(f'/entrega/comprobante/{nombre}/')
    
    return redirect('/entrega/verificar/')

def comprobante(request, nombre):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    equipo = next((e for e in equipos_registrados if e['cliente'] == nombre), None)
    diagnostico = next((d for d in DIAGNOSTICOS if d['equipo'] == nombre), None)
    
    if not equipo:
        messages.error(request, 'Equipo no encontrado.')
        return redirect('/entrega/verificar/')
    
    return render(request, 'entrega/comprobante.html', {
        'equipo': equipo,
        'diagnostico': diagnostico
    })