from django import forms
from .models import Estagiario

class EstagiarioForm(forms.ModelForm):
    class Meta:
        model = Estagiario
        fields = ['nome', 'matricula', 'email', 'telefone', 'curso']