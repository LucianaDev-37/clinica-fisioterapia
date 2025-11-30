from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_agendamentos, name='listar_agendamentos'),
    path('novo/', views.cadastrar_agendamento, name='cadastrar_agendamento'),
    path('editar/<int:id>/', views.editar_agendamento, name='editar_agendamento'),
    path('deletar/<int:id>/', views.deletar_agendamento, name='deletar_agendamento'),
]
