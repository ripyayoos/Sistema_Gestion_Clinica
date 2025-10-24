from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from recepcion.models import Equipo, Cliente
from diagnostico.models import Diagnostico 

@login_required
def entrega_home(request):
    """Página de inicio que lista equipos listos para entrega y el historial."""
    
    # Lista 1: Equipos Pendientes de Retiro (Estado LISTO)
    equipos_pendientes = Diagnostico.objects.filter(
        estado='LISTO'
    ).select_related('equipo', 'equipo__cliente') 
    
    # Lista 2: Historial de Equipos ENTREGADOS (Estado ENTREGADO)
    historial_entregados = Diagnostico.objects.filter(
        estado='ENTREGADO'
    ).select_related('equipo', 'equipo__cliente').order_by('-fecha_inicio') 
    
    context = {
        'equipos_pendientes': equipos_pendientes, 
        'historial_entregados': historial_entregados, 
        'usuario': request.user.username,
    }
    return render(request, 'entrega/home.html', context)

@login_required
def verificar_equipo(request):
    """READ: Permite buscar un equipo por S/N o RUT y listar el reporte de diagnóstico."""
    
    busqueda = request.GET.get('busqueda')
    diagnostico = None
    
    if busqueda:
        busqueda = busqueda.strip()
        
        try:
            equipo = Equipo.objects.get(num_serie__iexact=busqueda)
        except Equipo.DoesNotExist:
            try:
                cliente = Cliente.objects.get(rut__iexact=busqueda)
                equipo = cliente.equipos_recibidos.latest('recepcion__fecha_ingreso') 
            except (Cliente.DoesNotExist, Equipo.DoesNotExist):
                messages.error(request, f"No se encontró ningún equipo o cliente con la búsqueda '{busqueda}'.")
                return redirect('entrega:home')
            
        try:
            diagnostico = Diagnostico.objects.get(equipo=equipo)
        except Diagnostico.DoesNotExist:
            messages.warning(request, f"Equipo encontrado, pero no tiene diagnóstico registrado.")
            return redirect('entrega:home')

    context = {
        'diagnostico': diagnostico,
    }
    return render(request, 'entrega/verificar.html', context)

@login_required
def confirmar_entrega(request, pk):
    """UPDATE: Confirma que el cliente retiró el equipo y actualiza el estado a ENTREGADO."""
    
    diagnostico = get_object_or_404(Diagnostico.objects.select_related('equipo__cliente'), pk=pk)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                diagnostico.estado = 'ENTREGADO' 
                diagnostico.save()
                
            messages.success(request, f"Equipo S/N {diagnostico.equipo.num_serie} entregado y ciclo cerrado.")
            return redirect('entrega:reporte', pk=diagnostico.pk)
            
        except Exception as e:
            messages.error(request, f'Error al confirmar la entrega: {e}')
            return redirect('entrega:home')
    
    context = {'diagnostico': diagnostico}
    return render(request, 'entrega/confirmar_form.html', context)


@login_required
def reporte_entrega(request, pk):
    """READ: Genera el comprobante final de entrega."""
    diagnostico = get_object_or_404(Diagnostico.objects.select_related('equipo__cliente', 'tecnico_asignado'), pk=pk)
    
    if diagnostico.estado != 'ENTREGADO':
        messages.warning(request, "El equipo aún no ha sido marcado como entregado.")
        return redirect('entrega:home')
        
    return render(request, 'entrega/reporte.html', {
        'diagnostico': diagnostico,
    })