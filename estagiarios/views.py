from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Estagiario
from .forms import EstagiarioForm
from django.contrib import messages
from django.contrib.auth.models import User
from pacientes.models import Paciente
from agendamentos.models import Agendamento
from evolucoes.models import Evolucao
# -------------------------------
# REDIRECIONAMENTO PÓS-LOGIN
# -------------------------------
@login_required
def home_redirect(request):
    user = request.user
    if user.groups.filter(name='Gestores').exists():
        return redirect('painel_gestores')
    elif user.groups.filter(name='Estagiarios').exists():
        return redirect('painel_estagiarios')
    else:
        return redirect('listar_estagiarios')

# -------------------------------
# PAINÉIS (AGORA ENVIANDO OS DADOS)
# -------------------------------
@login_required
def painel_gestores(request):
    contexto = {
        'estagiarios': User.objects.filter(groups__name='Estagiarios'),
        'total_pacientes': Paciente.objects.count(),
        'total_estagiarios': Estagiario.objects.count(),
        'total_agendamentos': Agendamento.objects.count(),
        'total_evolucoes': Evolucao.objects.count(),
    }
    return render(request, 'estagiarios/dashboard_gestor.html', contexto)

@login_required
def painel_estagiarios(request):
    # ANTES: 'dashboard_estagiario.html'
    # AGORA: 'estagiarios/dashboard_estagiario.html'
    return render(request, 'estagiarios/dashboard_estagiario.html')
# -------------------------------
# CRUD ESTAGIÁRIOS
# -------------------------------
def listar_estagiarios(request):
    estagiarios = Estagiario.objects.all()
    return render(request, 'estagiarios/listar.html', {'estagiarios': estagiarios})

def cadastrar_estagiario(request):
    if request.method == 'POST':
        form = EstagiarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estagiário cadastrado com sucesso!')
            return redirect('listar_estagiarios')
    else:
        form = EstagiarioForm()
    return render(request, 'estagiarios/form.html', {'form': form})

def editar_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    if request.method == 'POST':
        form = EstagiarioForm(request.POST, instance=estagiario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estagiário Editado com sucesso!')
            return redirect('listar_estagiarios')
    else:
        form = EstagiarioForm(instance=estagiario)
    return render(request, 'estagiarios/form.html', {'form': form})

def deletar_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    if request.method == 'POST':
        estagiario.delete()
        messages.success(request, 'Estagiário deletado com sucesso!')
        return redirect('listar_estagiarios')
    return render(request, 'estagiarios/deletar.html', {'estagiario': estagiario})

# -------------------------------
# DETALHES DO ESTAGIÁRIO
# -------------------------------
def detalhes_estagiario(request, id):
    # Busca o estagiário pelo ID ou retorna 404 se não existir
    estagiario = get_object_or_404(Estagiario, id=id)
    return render(request, 'estagiarios/detalhes.html', {'estagiario': estagiario})
