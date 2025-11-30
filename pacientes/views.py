from django.shortcuts import render, redirect, get_object_or_404
from .models import Paciente
from .forms import PacienteForm

# Listar pacientes
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})

# Cadastrar paciente
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/cadastrar.html', {'form': form})

# Editar paciente
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/cadastrar.html', {'form': form})

# Deletar paciente
def deletar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('listar_pacientes')
    return render(request, 'pacientes/deletar.html', {'paciente': paciente})
