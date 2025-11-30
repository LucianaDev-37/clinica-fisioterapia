from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pacientes, name='listar_pacientes'),
    path('novo/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('deletar/<int:id>/', views.deletar_paciente, name='deletar_paciente'),
]
