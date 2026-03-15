from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Estagiario
from .forms import EstagiarioForm
from django.contrib import messages
from django.contrib.auth.models import User

# Importe os modelos dos outros apps
from pacientes.models import Paciente
from agendamentos.models import Agendamento
from evolucoes.models import Evolucao

# --- FUNÇÃO DE TESTE PARA SEGURANÇA ---
def eh_gestor(user):
    """Verifica se o usuário pertence ao grupo Gestores ou é admin."""
    return user.groups.filter(name='Gestores').exists() or user.is_superuser

# 1. FUNÇÃO PARA A RAIZ DO SITE
def pagina_inicial(request):
    if request.user.is_authenticated:
        return home_redirect(request)
    return render(request, 'pagina_inicial.html')

# 2. REDIRECIONAMENTO PÓS-LOGIN
@login_required
def home_redirect(request):
    user = request.user
    if eh_gestor(user):
        return redirect('dashboard_gestor')
    elif user.groups.filter(name='Estagiarios').exists():
        return redirect('dashboard_estagiario')
    else:
        # Se não tiver grupo, manda para uma área neutra ou logout
        return redirect('login')

# 3. DASHBOARD DO GESTOR (BLINDADO)
@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def dashboard_gestor(request):
    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'total_estagiarios': Estagiario.objects.count(),
        'total_agendamentos': Agendamento.objects.count(),
        'total_evolucoes': Evolucao.objects.count(),
    }
    return render(request, 'estagiarios/dashboard_gestor.html', contexto)

# 4. DASHBOARD DO ESTAGIÁRIO
@login_required
def dashboard_estagiario(request):
    return render(request, 'estagiarios/dashboard_estagiario.html')

# --- CRUD ESTAGIÁRIOS (TODAS BLINDADAS PARA GESTORES) ---

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def listar_estagiarios(request):
    busca = request.GET.get('search')
    estagiarios = Estagiario.objects.filter(nome__icontains=busca) if busca else Estagiario.objects.all()
    return render(request, 'estagiarios/listar.html', {'estagiarios': estagiarios})

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
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

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
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

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def deletar_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    if request.method == 'POST':
        estagiario.delete()
        messages.success(request, 'Estagiário deletado com sucesso!')
        return redirect('listar_estagiarios')
    return render(request, 'estagiarios/deletar.html', {'estagiario': estagiario})

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def detalhes_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    return render(request, 'estagiarios/detalhes.html', {'estagiario': estagiario})