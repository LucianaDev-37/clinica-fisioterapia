from django.shortcuts import render, redirect
from .models import Agendamento
from .forms import AgendamentoForm

def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'agendamentos/listar.html', {'agendamentos': agendamentos})

def cadastrar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamentos')
    else:
        form = AgendamentoForm()
    return render(request, 'agendamentos/cadastrar.html', {'form': form})

def editar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'agendamentos/editar.html', {'form': form})

def deletar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    agendamento.delete()
    return redirect('listar_agendamentos')
