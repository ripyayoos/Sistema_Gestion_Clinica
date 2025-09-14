from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('clave')

        if usuario == 'inacap' and clave == 'clinica2025':
            request.session['autenticado'] = True
            return redirect('/recepcion/registrar/')
        else:
            messages.error(request, 'Usuario o clave incorrectos.')

    return render(request, 'login/login.html')



def registrar_equipo(request):
    if not request.session.get('autenticado'):
        messages.error(request, 'Debes iniciar sesión para acceder.')
        return redirect('/login/')
    

    return render(request, 'registrar.html')