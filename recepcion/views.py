from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
# Importamos modelos de Recepción
from .models import Cliente, Equipo, Recepcion
from .forms import ClienteForm, EquipoForm, RecepcionForm 
# Importamos modelos de Diagnóstico para estadísticas del Dashboard
from diagnostico.models import Diagnostico, Tecnico 


# VISTAS CRUD DE RECEPCIÓN
# ==============================================================================

@login_required 
def recepcion_home(request):
    """READ: Dashboard de recepción."""
    total_equipos = Equipo.objects.count()
    
    # Contamos equipos en estados 'En Diagnóstico' o 'En Reparación' para el dashboard
    equipos_en_reparacion = Diagnostico.objects.filter(estado__in=['DIAGNOSTICO', 'REPARACION']).count()
    total_tecnicos = Tecnico.objects.count()

    context = {
        'total_equipos': total_equipos,
        'equipos_en_reparacion': equipos_en_reparacion,
        'total_tecnicos': total_tecnicos,
        'usuario': request.user.username
    }
    # RUTA CORREGIDA: Apunta a 'recepcion/templates/recepcion/home.html'
    return render(request, 'recepcion/home.html', context)

# --- CREAR: registrar_equipo ---
@login_required
def registrar_equipo(request):
    """CREATE: Registro de Cliente, Equipo y Recepción."""
    
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, prefix='cliente')
        equipo_form = EquipoForm(request.POST, prefix='equipo')
        recepcion_form = RecepcionForm(request.POST, prefix='recepcion')
        
        if cliente_form.is_valid() and equipo_form.is_valid() and recepcion_form.is_valid():
            try:
                with transaction.atomic():
                    # Lógica para obtener o crear/actualizar cliente
                    rut = cliente_form.cleaned_data['rut']
                    cliente, created = Cliente.objects.get_or_create(
                        rut=rut, defaults=cliente_form.cleaned_data
                    )
                    if not created:
                        cliente.nombre = cliente_form.cleaned_data['nombre']
                        cliente.apellido = cliente_form.cleaned_data['apellido']
                        cliente.email = cliente_form.cleaned_data['email']
                        cliente.telefono = cliente_form.cleaned_data['telefono']
                        cliente.save()

                    # Lógica para crear Equipo y Recepción
                    equipo = equipo_form.save(commit=False)
                    equipo.cliente = cliente
                    equipo.save()

                    recepcion = recepcion_form.save(commit=False)
                    recepcion.equipo = equipo
                    recepcion.save()
                
                messages.success(request, f'Equipo {equipo.num_serie} y cliente {cliente.nombre} registrados con éxito.')
                return redirect('recepcion:listado') 
                
            except Exception as e:
                messages.error(request, f'Error al registrar equipo: {e}')
                
        else:
            messages.error(request, 'Error en el formulario. Por favor, revise los campos.')
            
    else:
        cliente_form = ClienteForm(prefix='cliente')
        equipo_form = EquipoForm(prefix='equipo')
        recepcion_form = RecepcionForm(prefix='recepcion')

    context = {
        'cliente_form': cliente_form,
        'equipo_form': equipo_form,
        'recepcion_form': recepcion_form,
    }
    # RUTA CORREGIDA: renderiza 'recepcion/templates/recepcion/registrar.html'
    return render(request, 'recepcion/registrar.html', context)


# --- LEER: listado_equipos ---
@login_required
def listado_equipos(request):
    """READ: Lista todos los equipos y su estado de recepción."""
    equipos = Equipo.objects.all().select_related('cliente').prefetch_related('recepcion')
    
    context = {'equipos': equipos}
    # RUTA CORREGIDA: renderiza 'recepcion/templates/recepcion/listado.html'
    return render(request, 'recepcion/listado.html', context)

# --- LEER/ACTUALIZAR: detalle_equipo (Detalle y Edición) ---
@login_required
def detalle_equipo(request, pk):
    """READ/UPDATE: Muestra el detalle de un equipo y permite actualizar datos del cliente/equipo."""
    equipo = get_object_or_404(Equipo.objects.select_related('cliente', 'recepcion'), pk=pk)
    
    # Intenta obtener el diagnóstico para el link
    try:
        diagnostico_info = Diagnostico.objects.get(equipo=equipo)
    except Diagnostico.DoesNotExist:
        diagnostico_info = None

    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, prefix='cliente', instance=equipo.cliente)
        equipo_form = EquipoForm(request.POST, prefix='equipo', instance=equipo)
        
        if cliente_form.is_valid() and equipo_form.is_valid():
            cliente_form.save()
            equipo_form.save()
            messages.success(request, f'Datos del Equipo/Cliente actualizados para S/N: {equipo.num_serie}')
            return redirect('recepcion:detalle', pk=equipo.pk)
        else:
            messages.error(request, 'Error al actualizar los datos. Revise los formularios.')

    else:
        cliente_form = ClienteForm(prefix='cliente', instance=equipo.cliente)
        equipo_form = EquipoForm(prefix='equipo', instance=equipo)

    context = {
        'equipo': equipo,
        'cliente_form': cliente_form,
        'equipo_form': equipo_form,
        'diagnostico_info': diagnostico_info, # Pasamos la info de diagnóstico
    }
    # RUTA CORREGIDA: renderiza 'recepcion/templates/recepcion/detalle.html'
    return render(request, 'recepcion/detalle.html', context)

# --- ELIMINAR: eliminar_equipo ---
@login_required
def eliminar_equipo(request, pk):
    """DELETE: Elimina un equipo y su cliente asociado (si el cliente no tiene más equipos)."""
    equipo = get_object_or_404(Equipo, pk=pk)
    cliente = equipo.cliente 

    if request.method == 'POST':
        equipo_num_serie = equipo.num_serie
        equipo.delete()
        
        if cliente.equipos_recibidos.count() == 0:
            cliente.delete()
        
        messages.success(request, f'Equipo con S/N: {equipo_num_serie} eliminado correctamente.')
        return redirect('recepcion:listado')

    context = {'equipo': equipo}
    # RUTA CORREGIDA: renderiza 'recepcion/templates/recepcion/confirm_delete.html'
    return render(request, 'recepcion/confirm_delete.html', context)