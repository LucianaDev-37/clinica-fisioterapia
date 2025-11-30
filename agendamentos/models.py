from django.db import models
from pacientes.models import Paciente
from estagiarios.models import Estagiario

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('reagendado', 'Reagendado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    estagiario = models.ForeignKey(Estagiario, on_delete=models.SET_NULL, null=True)
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado')
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.paciente.nome} - {self.data} {self.hora}"
