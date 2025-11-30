from django.db import models
from pacientes.models import Paciente
from estagiarios.models import Estagiario

class Evolucao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    estagiario = models.ForeignKey(Estagiario, on_delete=models.SET_NULL, null=True)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evolução de {self.paciente.nome} em {self.data.strftime('%d/%m/%Y')}"
