from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Cliente, Equipo, Recepcion
from .forms import ClienteForm, EquipoForm, RecepcionForm 
from diagnostico.models import Diagnostico, Tecnico 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# VISTAS CRUD HTML
# ==============================================================================

@login_required 
def recepcion_home(request):
    """READ: Dashboard de recepción."""
    total_equipos = Equipo.objects.count()
    
    # Contamos equipos en estados 'En Diagnóstico' o 'En Reparación'
    equipos_en_reparacion = Diagnostico.objects.filter(estado__in=['DIAGNOSTICO', 'REPARACION']).count()
    total_tecnicos = Tecnico.objects.count()

    context = {
        'total_equipos': total_equipos,
        'equipos_en_reparacion': equipos_en_reparacion,
        'total_tecnicos': total_tecnicos,
        'usuario': request.user.username
    }
    return render(request, 'recepcion/home.html', context)

# --- CREAR: registrar_equipo ---
@login_required
def registrar_equipo(request):
    """CREATE: Registro de Cliente, Equipo y Recepción en una sola transacción."""
    
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, prefix='cliente')
        equipo_form = EquipoForm(request.POST, prefix='equipo')
        recepcion_form = RecepcionForm(request.POST, prefix='recepcion')
        
        if cliente_form.is_valid() and equipo_form.is_valid() and recepcion_form.is_valid():
            try:
                with transaction.atomic():
                    rut = cliente_form.cleaned_data['rut']
                    cliente, created = Cliente.objects.get_or_create(
                        rut=rut,
                        defaults=cliente_form.cleaned_data
                    )
                    if not created:
                        cliente.nombre = cliente_form.cleaned_data['nombre']
                        cliente.apellido = cliente_form.cleaned_data['apellido']
                        cliente.email = cliente_form.cleaned_data['email']
                        cliente.telefono = cliente_form.cleaned_data['telefono']
                        cliente.save()

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
    return render(request, 'recepcion/registrar.html', context)


# --- LEER: listado_equipos ---
@login_required
def listado_equipos(request):
    """READ: Lista todos los equipos y su estado de recepción (Historial de equipos ingresados)."""
    # Consulta todos los equipos ingresados
    equipos = Equipo.objects.all().select_related('cliente').prefetch_related('recepcion')
    
    context = {'equipos': equipos}
    return render(request, 'recepcion/listado.html', context)

# --- LEER/ACTUALIZAR: detalle_equipo (Detalle y Edición) ---
@login_required
def detalle_equipo(request, pk):
    """READ/UPDATE: Muestra el detalle de un equipo y permite actualizar datos del cliente/equipo."""
    equipo = get_object_or_404(Equipo.objects.select_related('cliente', 'recepcion'), pk=pk)
    
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
        'diagnostico_info': diagnostico_info,
    }
    return render(request, 'recepcion/detalle.html', context)

# --- ELIMINAR: eliminar_equipo ---
@login_required
def eliminar_equipo(request, pk):
    """DELETE: Elimina un equipo y su cliente asociado."""
    equipo = get_object_or_404(Equipo, pk=pk)
    cliente = equipo.cliente 

    if request.method == 'POST':
        try:
            with transaction.atomic(): 
                equipo_num_serie = equipo.num_serie
                equipo.delete()
                
                # Solo elimina al cliente si no tiene otros equipos registrados
                if cliente.equipos_recibidos.count() == 0:
                    cliente.delete()
            
            messages.success(request, f'Equipo con S/N: {equipo_num_serie} eliminado correctamente.')
            return redirect('recepcion:listado')

        except Exception as e:
             messages.error(request, f'Error al eliminar el equipo: {e}')
             return redirect('recepcion:detalle', pk=equipo.pk)

    context = {'equipo': equipo}
    return render(request, 'recepcion/confirm_delete.html', context)

# --- API ENDPOINTS (FUNCIONES REST) ---
# ==============================================================================

# API: GET - Obtener detalle por número de serie
@csrf_exempt
def api_detalle_recepcion(request, num_serie):
    """API GET: Obtiene el detalle de una recepción por número de serie."""
    if request.method == "GET":
        try:
            equipo = Equipo.objects.get(num_serie=num_serie)
            recepcion = Recepcion.objects.get(equipo=equipo)
            
            data = {
                "num_serie": equipo.num_serie,
                "tipo": equipo.tipo,
                "marca": equipo.marca,
                "cliente": {
                    "rut": equipo.cliente.rut,
                    "nombre": equipo.cliente.nombre,
                    "telefono": equipo.cliente.telefono,
                },
                "problema_reportado": recepcion.problema_reportado,
                "fecha_ingreso": recepcion.fecha_ingreso.isoformat(),
            }
            return JsonResponse(data)
        except Equipo.DoesNotExist:
            return JsonResponse({"error": "Equipo no encontrado"}, status=404)
        except Recepcion.DoesNotExist:
            return JsonResponse({"error": "Recepción no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


# API: POST - Crear recepción
@csrf_exempt
def api_crear_recepcion(request):
    """POST: Crear cliente + equipo + recepción por API (JSON)"""
    
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        # 1. Cliente
        cliente, creado = Cliente.objects.get_or_create(
            rut=data["rut"],
            defaults={
                "nombre": data["nombre"],
                "apellido": data["apellido"],
                "email": data["email"],
                "telefono": data["telefono"]
            }
        )

        # 2. Equipo
        equipo = Equipo.objects.create(
            tipo=data["tipo"],
            marca=data["marca"],
            num_serie=data["num_serie"],
            cliente=cliente
        )

        # 3. Recepción
        recepcion = Recepcion.objects.create(
            equipo=equipo,
            problema_reportado=data["problema"]
        )

        return JsonResponse({
            "mensaje": "Recepción creada correctamente",
            "recepcion": {
                "num_serie": equipo.num_serie,
                "cliente": f"{cliente.nombre} {cliente.apellido}",
                "fecha_ingreso": recepcion.fecha_ingreso
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

# API: PUT - Actualizar recepción
@csrf_exempt
def api_actualizar_recepcion(request, num_serie):
    """PUT: Actualizar el registro de recepción por API (JSON)"""

    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        equipo = Equipo.objects.get(num_serie=num_serie)
        recepcion = Recepcion.objects.get(equipo=equipo)

        # Actualizar problema
        if "problema" in data:
            recepcion.problema_reportado = data["problema"]

        recepcion.save()

        return JsonResponse({"mensaje": "Recepción actualizada correctamente"})

    except Equipo.DoesNotExist:
        return JsonResponse({"error": "Equipo no encontrado"}, status=404)
    
    except Recepcion.DoesNotExist:
        return JsonResponse({"error": "Recepción no encontrada"}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# API: DELETE - Eliminar por número de serie
@csrf_exempt
def api_eliminar_recepcion(request, num_serie):
    """API DELETE: Elimina un registro de recepción por número de serie."""
    if request.method == "DELETE":
        try:
            equipo = Equipo.objects.get(num_serie=num_serie)
            equipo.delete()
            return JsonResponse({"mensaje": f"Equipo S/N {num_serie} eliminado."}, status=204)
        except Equipo.DoesNotExist:
            return JsonResponse({"error": "Equipo no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)