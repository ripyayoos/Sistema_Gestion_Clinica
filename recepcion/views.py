from django.shortcuts import render, redirect
from django.contrib import messages

equipos_registrados = []

def registrar_equipo(request):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        tipo_equipo = request.POST.get('tipo_equipo')
        problema = request.POST.get('problema')
        
        equipo = {
            'cliente': cliente,
            'tipo_equipo': tipo_equipo,
            'problema': problema,
            'estado': 'Recibido',
            'id': len(equipos_registrados) + 1
        }
        
        equipos_registrados.append(equipo)
        messages.success(request, 'Equipo registrado correctamente')
        return redirect('/recepcion/listado/')
    
    return render(request, 'recepcion/registrar.html')

def listado_equipos(request):
    if not request.session.get('autenticado'):
        return redirect('/')
    return render(request, 'recepcion/listado.html', {'equipos': equipos_registrados})

def detalle_equipo(request, nombre):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    equipo = next((eq for eq in equipos_registrados if eq['cliente'] == nombre), None)
    return render(request, 'recepcion/detalle.html', {'equipo': equipo})