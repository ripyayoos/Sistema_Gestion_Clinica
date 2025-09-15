from django.shortcuts import render, redirect
from django.contrib import messages
from recepcion.views import equipos_registrados

DIAGNOSTICOS = []

def asignar_tarea(request):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    estudiantes = ['Alumno A', 'Alumno B', 'Alumno C']
    return render(request, 'diagnostico/asignar.html', {
        'equipos': equipos_registrados,
        'estudiantes': estudiantes
    })

def evaluar_diagnostico(request):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    if request.method == 'POST':
        estudiante = request.POST.get('estudiante')
        equipo_nombre = request.POST.get('equipo')
        diagnostico = request.POST.get('diagnostico')
        solucion = request.POST.get('solucion')
        tipo_solucion = 'correctiva' if request.POST.get('tipo') == 'correctiva' else 'preventiva'
        
        DIAGNOSTICOS.append({
            'estudiante': estudiante,
            'equipo': equipo_nombre,
            'diagnostico': diagnostico,
            'solucion': solucion,
            'tipo': tipo_solucion,
        })
        
        messages.success(request, 'Diagnóstico registrado correctamente')
        return redirect('/diagnostico/listado/')
    
    return redirect('/diagnostico/asignar/')

def listado_diagnosticos(request):
    if not request.session.get('autenticado'):
        return redirect('/')
    
    return render(request, 'diagnostico/listado.html', {
        'diagnosticos': DIAGNOSTICOS
    })