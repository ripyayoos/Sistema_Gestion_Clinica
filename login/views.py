from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy # Importar reverse_lazy

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Lógica de autenticación manual: inacap/clinica2025
        if username == 'inacap' and password == 'clinica2025':
            
            try:
                user = User.objects.get(username=username) 
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email='inacap@clinica.cl', password='clinica2025')
                user.is_superuser = True
                user.is_staff = True
                user.save()
            
            auth_login(request, user)
            
            # Usamos reverse_lazy para la redirección
            return redirect(reverse_lazy('recepcion:home')) 
        else:
            messages.error(request, 'Credenciales incorrectas')
            # RUTA CORREGIDA: Si falla la autenticación, vuelve a renderizar el formulario.
            return render(request, 'login.html') # <--- ¡CAMBIADO A 'login.html'!
    
    # RUTA CORREGIDA: Si es un GET, renderiza el formulario.
    return render(request, 'login.html') # <--- ¡CAMBIADO A 'login.html'!

def logout_view(request):
    auth_logout(request) 
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login:login')