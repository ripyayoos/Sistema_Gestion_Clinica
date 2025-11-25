from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse_lazy


from recepcion.models import Equipo
from .models import Tecnico, Diagnostico, Servicio
from .forms import DiagnosticoForm 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# VISTAS CRUD DE DIAGNÓSTICO
# ==============================================================================

@login_required
def diagnostico_home(request):
    """READ: Dashboard principal de Diagnóstico."""
    total_diagnosticos = Diagnostico.objects.count()
    equipos_listos = Diagnostico.objects.filter(estado='LISTO').count()
    tecnicos_activos = Tecnico.objects.annotate(
        num_diagnosticos=Count('diagnosticos_realizados')
    ).count()

    context = {
        'total_diagnosticos': total_diagnosticos,
        'equipos_listos': equipos_listos,
        'tecnicos_activos': tecnicos_activos,
        'usuario': request.user.username
    }
    return render(request, 'diagnostico/home.html', context)


@login_required
def listado_diagnosticos(request):
    """READ: Lista todos los diagnósticos pendientes/en curso."""
    diagnosticos = Diagnostico.objects.all().select_related('equipo', 'tecnico_asignado')
    
    context = {'diagnosticos': diagnosticos}
    return render(request, 'diagnostico/listado.html', context)

@login_required
def asignar_diagnostico(request, equipo_pk):
    """CREATE: Asigna técnico y registra el diagnóstico inicial a un equipo (PK)"""
    equipo = get_object_or_404(Equipo, pk=equipo_pk)
    
    try:
        diagnostico_existente = Diagnostico.objects.get(equipo=equipo)
        messages.warning(request, f"El equipo S/N {equipo.num_serie} ya tiene un diagnóstico asignado.")
        return redirect('diagnostico:detalle', pk=diagnostico_existente.pk)
    except Diagnostico.DoesNotExist:
        pass 

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST) 
        if form.is_valid():
            diagnostico = form.save(commit=False)
            diagnostico.equipo = equipo
            diagnostico.save()
            
            form.save_m2m() # Guarda la relación M2M (Servicios)
            
            messages.success(request, f'Diagnóstico asignado a {diagnostico.tecnico_asignado.nombre}')
            return redirect('diagnostico:listado') 
        else:
            messages.error(request, 'Error al procesar el formulario.')
            
    else:
        form = DiagnosticoForm()

    context = {
        'equipo': equipo,
        'form': form,
        'servicios': Servicio.objects.all(),
        'tecnicos': Tecnico.objects.all()
    }
    return render(request, 'diagnostico/asignar_form.html', context)


@login_required
def detalle_diagnostico(request, pk):
    """READ/UPDATE/DELETE: Vista de detalle para gestionar el diagnóstico."""
    diagnostico = get_object_or_404(Diagnostico.objects.select_related('equipo', 'tecnico_asignado'), pk=pk)

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, instance=diagnostico)
        if form.is_valid():
            # CORRECCIÓN DEL ATTRIBUTE ERROR:
            diagnostico_guardado = form.save(commit=False)
            diagnostico_guardado.save() 
            form.save_m2m() 
            
            messages.success(request, 'Diagnóstico actualizado con éxito.')
            return redirect('diagnostico:detalle', pk=pk)
        else:
            messages.error(request, 'Error al actualizar el diagnóstico.')
            
    else:
        form = DiagnosticoForm(instance=diagnostico)

    context = {
        'diagnostico': diagnostico,
        'form': form,
        'servicios_disponibles': Servicio.objects.all(),
    }
    return render(request, 'diagnostico/detalle.html', context)

@login_required
def eliminar_diagnostico(request, pk):
    """DELETE: Elimina un registro de diagnóstico."""
    diagnostico = get_object_or_404(Diagnostico, pk=pk)
    if request.method == 'POST':
        diagnostico.delete()
        messages.success(request, f'Diagnóstico para S/N: {diagnostico.equipo.num_serie} eliminado.')
        return redirect('diagnostico:listado')
        
    return render(request, 'diagnostico/confirm_delete.html', {'diagnostico': diagnostico})

def crear_diagnostico(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        nuevo = Diagnostico.objects.create(
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            estado="pendiente"
        )
        return JsonResponse({"mensaje": "Diagnóstico creado", "id": nuevo.id})

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def actualizar_diagnostico(request, pk):
    diagnostico = get_object_or_404(Diagnostico, pk=pk)

    if request.method == "PUT":
        data = json.loads(request.body)

        diagnostico.titulo = data.get("titulo", diagnostico.titulo)
        diagnostico.descripcion = data.get("descripcion", diagnostico.descripcion)
        diagnostico.estado = data.get("estado", diagnostico.estado)

        diagnostico.save()

        return JsonResponse({"mensaje": "Diagnóstico actualizado"})

    return JsonResponse({"error": "Método no permitido"}, status=405)