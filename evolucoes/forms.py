from django import forms
from .models import Evolucao

class EvolucaoForm(forms.ModelForm):
    class Meta:
        model = Evolucao
        fields = ['paciente', 'estagiario', 'descricao']
        
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'estagiario': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Relate aqui o atendimento e a evolução do paciente...'
            }),
        }