from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy

# Importamos modelos desde otras apps
from recepcion.models import Equipo, Cliente
from diagnostico.models import Diagnostico 
# NOTA: Eliminamos las importaciones obsoletas de listas globales.

@login_required
def entrega_home(request):
    """Página de inicio que lista equipos listos para entrega."""
    
    # Busca diagnósticos cuyo estado es 'LISTO' (asumiendo que LISTO es el estado final)
    equipos_listos = Diagnostico.objects.filter(
        estado='LISTO'
    ).select_related('equipo', 'equipo__cliente') # Precarga Equipo y Cliente
    
    context = {
        'equipos_listos': equipos_listos,
        'usuario': request.user.username,
    }
    return render(request, 'entrega/home.html', context)

@login_required
def verificar_equipo(request):
    """READ: Permite buscar un equipo por S/N o RUT y listar el reporte de diagnóstico."""
    
    # Usaremos el S/N del equipo o el RUT del cliente para la búsqueda
    busqueda = request.GET.get('busqueda')
    diagnostico = None
    
    if busqueda:
        busqueda = busqueda.strip()
        
        try:
            # 1. Buscar por Número de Serie del Equipo
            equipo = Equipo.objects.get(num_serie__iexact=busqueda)
        except Equipo.DoesNotExist:
            try:
                # 2. Buscar por RUT del Cliente
                cliente = Cliente.objects.get(rut__iexact=busqueda)
                # Obtenemos el equipo más reciente de ese cliente
                equipo = cliente.equipos_recibidos.latest('recepcion__fecha_ingreso') 
            except (Cliente.DoesNotExist, Equipo.DoesNotExist):
                messages.error(request, f"No se encontró ningún equipo o cliente con la búsqueda '{busqueda}'.")
                return redirect('entrega:home')
            
        # 3. Una vez que tenemos el equipo, buscamos su diagnóstico (si existe)
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
        # Se asume que al presionar el botón de confirmar, el estado final es 'ENTREGADO'
        try:
            with transaction.atomic():
                diagnostico.estado = 'ENTREGADO' # Asumimos que 'ENTREGADO' es un estado final
                diagnostico.save()
                
                # Opcional: Registrar la fecha de entrega en un campo (si lo hubieras añadido a Diagnostico/Equipo)
                
            messages.success(request, f"Equipo S/N {diagnostico.equipo.num_serie} entregado y ciclo cerrado.")
            return redirect('entrega:reporte', pk=pk) # Redirigir al comprobante final
            
        except Exception as e:
            messages.error(request, f'Error al confirmar la entrega: {e}')
            return redirect('entrega:home')
    
    # GET: Pide confirmación
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
        # Puedes incluir aquí la fecha/hora actual de la generación del reporte
    })