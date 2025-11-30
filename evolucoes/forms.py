from django import forms
from .models import Evolucao

class EvolucaoForm(forms.ModelForm):
    class Meta:
        model = Evolucao
        fields = ['paciente', 'estagiario', 'descricao']
