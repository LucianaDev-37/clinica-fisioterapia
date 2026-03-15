from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'estagiario', 'data', 'hora', 'observacoes']
        
        # formulário ficar funcional:
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'estagiario': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }