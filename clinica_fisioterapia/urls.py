from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# Ajustei os nomes
from estagiarios.views import pagina_inicial, dashboard_gestor, dashboard_estagiario
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pagina_inicial, name='pagina_inicial'),

    # Dashboards
    path('gestor/', dashboard_gestor, name='dashboard_gestor'),
    path('estagiario/', dashboard_estagiario, name='dashboard_estagiario'),

    # Apps
    path('estagiarios/', include('estagiarios.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('agendamentos/', include('agendamentos.urls')),
    path('evolucoes/', include('evolucoes.urls')),

    # Autenticação Completa
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Mantemos suas rotas customizadas:
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]