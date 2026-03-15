from django.db import models
from django.contrib.auth.models import User

# --- LOG DE ACESSOS (TENTATIVAS) ---
class AuditoriaAcesso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pagina_tentada = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField(default=False)

    def __str__(self):
        status = "SUCESSO" if self.sucesso else "NEGADO"
        return f"{self.usuario} - {self.pagina_tentada} ({status})"

# --- LOG DE ALTERAÇÃO DE DADOS (MUTATION LOG) ---
class LogAlteracao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tabela = models.CharField(max_length=100) # Ex: 'Estagiario' ou 'Paciente'
    registro_id = models.IntegerField()
    acao = models.CharField(max_length=10) # 'CREATE', 'UPDATE', 'DELETE'
    data_hora = models.DateTimeField(auto_now_add=True)
    valor_antigo = models.TextField(null=True, blank=True)
    valor_novo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.acao} em {self.tabela} por {self.usuario}"

# Seus dados de estagiários permanecem iguais
class Estagiario(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    curso = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"