from django.shortcuts import render, redirect
from django.contrib import messages
from ..recepcion.views import EQUIPOS
from ..utils import login_required_session


# Create your views here.
DIAGNOSTICOS = []

@login_required_session
def asignar_tarea(request):
    estudiantes = ['Alumno A', 'Alumno B', 'Alumno C']
    return render(request, 'diagnostico/asignar.html', {'equipos': EQUIPOS, 'estudiantes': estudiantes})

@login_required_session
def evaluar_diagnostico(request):
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
        messages.success(request, 'Diagnóstico registrado.')
        return redirect('listado_diagnosticos')
    return redirect('asignar')

@login_required_session
def listado_diagnosticos(request):
    return render(request, 'diagnostico/listado.html', {'diagnosticos': DIAGNOSTICOS})
