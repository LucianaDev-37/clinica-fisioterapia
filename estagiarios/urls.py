from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_estagiarios, name='listar_estagiarios'),
    path('cadastrar/', views.cadastrar_estagiario, name='cadastrar_estagiario'),
    path('editar/<int:id>/', views.editar_estagiario, name='editar_estagiario'),
    path('deletar/<int:id>/', views.deletar_estagiario, name='deletar_estagiario'),

    # Novas rotas para redirecionamento e painéis
    path('home/', views.home_redirect, name='home_redirect'),
    path('painel-gestores/', views.painel_gestores, name='painel_gestores'),
    path('painel-estagiarios/', views.painel_estagiarios, name='painel_estagiarios'),
]

