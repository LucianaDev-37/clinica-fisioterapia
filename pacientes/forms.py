from django import forms
from .models import Paciente
#criação e edição dos pacientes na web.
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'telefone', 'data_nascimento', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
