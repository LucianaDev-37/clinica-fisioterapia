from django.urls import path
from . import views

urlpatterns = [
    # Página de entrada (Login)
    path('', views.listar_estagiarios, name='listar_estagiarios'), # Ou sua página inicial
    
    # CRUD de Estagiários
    path('cadastrar/', views.cadastrar_estagiario, name='cadastrar_estagiario'),
    path('editar/<int:id>/', views.editar_estagiario, name='editar_estagiario'),
    path('deletar/<int:id>/', views.deletar_estagiario, name='deletar_estagiario'),
    path('<int:id>/', views.detalhes_estagiario, name='detalhes_estagiario'),

    # O "Cérebro" do Redirecionamento
    path('home/', views.home_redirect, name='home_redirect'),

    # Painéis Específicos
    path('painel-gestores/', views.painel_gestores, name='painel_gestores'),
    path('painel-estagiarios/', views.painel_estagiarios, name='painel_estagiarios'),
]