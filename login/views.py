from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'inacap' and password == 'clinica2025':
            request.session['autenticado'] = True
            return redirect('/recepcion/registrar/')  # ✅ URL absoluta
        else:
            messages.error(request, 'Credenciales incorrectas')
            return redirect('/')
    
    return render(request, 'login/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('/')