from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # Importe o cadeado
from .models import Agendamento
from .forms import AgendamentoForm

# -------------------------------
# LISTAR AGENDAMENTOS
# -------------------------------
@login_required  # Protege a listagem
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'agendamentos/listar.html', {'agendamentos': agendamentos})

# -------------------------------
# CADASTRAR AGENDAMENTO
# -------------------------------
@login_required  # Protege o cadastro
def cadastrar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamentos')
    else:
        form = AgendamentoForm()
    return render(request, 'agendamentos/form.html', {'form': form})

# -------------------------------
# EDITAR AGENDAMENTO
# -------------------------------
@login_required  # Protege a edição
def editar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'agendamentos/form.html', {'form': form})

# -------------------------------
# DELETAR AGENDAMENTO
# -------------------------------
@login_required  # Protege a exclusão
def deletar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    agendamento.delete()
    return redirect('listar_agendamentos')