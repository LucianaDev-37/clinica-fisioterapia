from django.urls import path
from . import views

urlpatterns = [
    # ESSA É A LINHA QUE ESTÁ FALTANDO:
    path('home-redirect/', views.home_redirect, name='home_redirect'),

    # Painéis
    path('painel-gestores/', views.dashboard_gestor, name='dashboard_gestor'),
    path('painel-estagiarios/', views.dashboard_estagiario, name='dashboard_estagiario'),
    
    # CRUD Estagiários
    path('', views.listar_estagiarios, name='listar_estagiarios'),
    path('cadastrar/', views.cadastrar_estagiario, name='cadastrar_estagiario'),
    path('editar/<int:id>/', views.editar_estagiario, name='editar_estagiario'),
    path('deletar/<int:id>/', views.deletar_estagiario, name='deletar_estagiario'),
    path('detalhes/<int:id>/', views.detalhes_estagiario, name='detalhes_estagiario'),
]