from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from estagiarios.views import home_redirect, painel_gestores, painel_estagiarios
from django.shortcuts import redirect

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Raiz do site: redireciona para /home/
    path('', lambda request: redirect('home_redirect'), name='pagina_inicial'),

    # Dashboard
    path('home/', home_redirect, name='home_redirect'),
    path('gestor/', painel_gestores, name='dashboard_gestor'),
    path('estagiario/', painel_estagiarios, name='dashboard_estagiario'),

    # Apps
    path('estagiarios/', include('estagiarios.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('agendamentos/', include('agendamentos.urls')),
    path('evolucoes/', include('evolucoes.urls')),

    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
