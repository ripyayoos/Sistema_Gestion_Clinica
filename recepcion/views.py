from django.shortcuts import render, redirect
from django.contrib import messages
from .data import EQUIPOS

# Formulario para registrar equipo
def registrar(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        tipo = request.POST.get("tipo")
        problema = request.POST.get("problema")

        if nombre and tipo and problema:
            equipo = {
                "nombre": nombre,
                "tipo": tipo,
                "problema": problema
            }
            EQUIPOS.append(equipo)
            messages.success(request, "✅ Equipo registrado correctamente")
            return redirect("listado_equipos")
        else:
            messages.error(request, "⚠️ Debes completar todos los campos")

    return render(request, "recepcion/registrar.html")


# Listado de equipos
def listado(request):
    context = {"equipos": EQUIPOS}
    return render(request, "recepcion/listado.html", context)


# Detalle de un equipo por nombre
def detalle(request, nombre):
    equipo = next((e for e in EQUIPOS if e["nombre"] == nombre), None)
    if not equipo:
        messages.error(request, f"⚠️ No se encontró el equipo de {nombre}")
        return redirect("listado_equipos")

    return render(request, "recepcion/detalle.html", {"equipo": equipo})
