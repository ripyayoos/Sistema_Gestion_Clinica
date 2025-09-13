from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validación de usuario y contraseña predefinidos
        if username == 'inacap' and password == 'clinica2025':
            request.session['autenticado'] = True
            return redirect('/recepcion/registrar/')
        else:
            messages.error(request, 'Usuario o clave incorrectos.')

    return render(request, 'login.html')


# Vista protegida
def registrar_equipo(request):
    if not request.session.get('autenticado'):
        messages.error(request, 'Debes iniciar sesión para acceder.')
        return redirect('/login/')
    
    # Aquí iría la lógica de registrar equipo
    return render(request, 'registrar.html')