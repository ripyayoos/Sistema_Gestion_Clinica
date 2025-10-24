from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = 'login' # ¡Añadir el namespace!

urlpatterns = [
    # Si alguien entra a la raíz del proyecto (/)
    path('', lambda request: redirect('login/'), name='home_redirect'), 
    
    # La vista de login que usa tu lógica manual
    path('login/', views.login_view, name='login'),
    
    # La vista de logout
    path('logout/', views.logout_view, name='logout'), 
]