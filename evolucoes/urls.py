from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_evolucoes, name='listar_evolucoes'),
    path('nova/', views.cadastrar_evolucao, name='cadastrar_evolucao'),
    path('editar/<int:id>/', views.editar_evolucao, name='editar_evolucao'),
    path('deletar/<int:id>/', views.deletar_evolucao, name='deletar_evolucao'),
]
