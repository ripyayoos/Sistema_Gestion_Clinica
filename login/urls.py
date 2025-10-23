from django.urls import path
from . import views
from django.shortcuts import redirect
from django.urls import reverse_lazy

app_name = 'login' 

urlpatterns = [
    path('', lambda request: redirect(reverse_lazy('login:login')), name='home_redirect'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
]