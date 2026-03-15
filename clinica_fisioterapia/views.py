from django.shortcuts import render, redirect
from agendamentos.models import Agendamento
from pacientes.models import Paciente
from estagiarios.models import Estagiario
from evolucoes.models import Evolucao
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# 1. Ajuste na Página Inicial para redirecionar quem já está logado
def pagina_inicial(request):
    if request.user.is_authenticated:
        return redirecionar_dashboard(request)
    return render(request, 'pagina_inicial.html')

# 2. O seu "Guarda de Trânsito" (Mantido e organizado)
def redirecionar_dashboard(request):
    user = request.user
    
    if not user.is_authenticated:
        return redirect('login')

    if user.groups.filter(name='Gestores').exists():
        return redirect('dashboard_gestor')

    if user.groups.filter(name='Estagiarios').exists():
        return redirect('dashboard_estagiario')

    # Se estiver logado mas sem grupo, pode mandar para uma página padrão ou login
    return redirect('login')


# 3. Dashboard do Gestor (Com os contadores automáticos)
@login_required
def dashboard_gestor(request):
    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'total_estagiarios': Estagiario.objects.count(),
        'total_agendamentos': Agendamento.objects.count(),
        'total_evolucoes': Evolucao.objects.count(),
    }
    return render(request, 'dashboard_gestor.html', contexto)


# 4. Dashboard do Estagiário (Com filtros específicos)
@login_required
def dashboard_estagiario(request):
    user = request.user
    contexto = {
        'total_pacientes': 0,
        'total_agendamentos': 0,
        'total_evolucoes': 0,
    }
    
    try:
        # Busca o perfil de estagiário do usuário logado
        estagiario_logado = Estagiario.objects.get(user=user)

        # Filtra apenas o que pertence a este estagiário
        contexto['total_pacientes'] = Paciente.objects.filter(
            estagiario_responsavel=estagiario_logado
        ).count()

        contexto['total_agendamentos'] = Agendamento.objects.filter(
            estagiario=estagiario_logado
        ).count()

        contexto['total_evolucoes'] = Evolucao.objects.filter(
            estagiario=estagiario_logado
        ).count()

    except ObjectDoesNotExist:
        # Se o usuário não for estagiário, os zeros do contexto serão exibidos
        pass
    except Exception as e:
        print(f"Erro no dashboard do estagiário: {e}") 

    return render(request, 'dashboard_estagiario.html', contexto)