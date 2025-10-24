from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy

def login_view(request):
    """Vista que maneja la autenticación manual (inacap/clinica2025)."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'inacap' and password == 'clinica2025':
            try:
                user = User.objects.get(username=username) 
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email='inacap@clinica.cl', password='clinica2025')
                user.is_superuser = True
                user.is_staff = True
                user.save()
            
            auth_login(request, user)
            
            return redirect(reverse_lazy('recepcion:home'))
        else:
            messages.error(request, 'Credenciales incorrectas')
            return render(request, 'login.html') 
    
    return render(request, 'login.html')

def logout_view(request):
    """Cierra la sesión."""
    auth_logout(request) 
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login:login')