from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # IMPORTANTE: Adicione esta linha
from .models import Paciente
from .forms import PacienteForm

# Listar pacientes
@login_required  # Adicione este "cadeado"
def listar_pacientes(request):
    busca = request.GET.get('search')
    
    if busca:
        pacientes = Paciente.objects.filter(nome__icontains=busca)
    else:
        pacientes = Paciente.objects.all()
        
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})

# Cadastrar paciente
@login_required  # Adicione este "cadeado"
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/form.html', {'form': form})

# Editar paciente
@login_required  # Adicione este "cadeado"
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/form.html', {'form': form})

# Deletar paciente
@login_required  # Adicione este "cadeado"
def deletar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('listar_pacientes')
    return redirect('listar_pacientes')