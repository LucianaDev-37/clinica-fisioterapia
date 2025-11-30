from django.shortcuts import render, redirect
from agendamentos.models import Agendamento
from pacientes.models import Paciente
from estagiarios.models import Estagiario
from evolucoes.models import Evolucao
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist # Útil para tratamento de erro
def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')
def redirecionar_dashboard(request):
    user = request.user
    
    if not user.is_authenticated:
        return redirect('login')

    if user.groups.filter(name='Gestores').exists():
        return redirect('dashboard_gestor')

    if user.groups.filter(name='Estagiarios').exists():
        return redirect('dashboard_estagiario')

    return redirect('login')


# Dashboard do Gestor
@login_required
def dashboard_gestor(request):
    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'total_estagiarios': Estagiario.objects.count(),
        'total_agendamentos': Agendamento.objects.count(),
        'total_evolucoes': Evolucao.objects.count(),
    }
    return render(request, 'dashboard_gestor.html', contexto)


# Dashboard do Estagiário
@login_required
def dashboard_estagiario(request):
    user = request.user
    contexto = {
        # Inicializa o contexto com 0 para evitar erros no template caso a busca falhe
        'total_pacientes': 0,
        'total_agendamentos': 0,
        'total_evolucoes': 0,
    }
    try:
        # 1. Encontra o objeto Estagiário associado ao usuário logado
        # CRÍTICO: Assume-se que o modelo Estagiario tem um campo FK chamado 'user'
        estagiario_logado = Estagiario.objects.get(user=user)

        # 2. CALCULA OS TOTAIS FILTRADOS PELO estagiario_logado
        
        # Pacientes (Filtra pacientes onde o 'estagiario_responsavel' é o estagiário logado)
        contexto['total_pacientes'] = Paciente.objects.filter(
            estagiario_responsavel=estagiario_logado
        ).count()

        # Agendamentos (Filtra agendamentos relacionados ao estagiário)
        # Opcional: Você pode filtrar apenas os agendamentos FUTUROS adicionando:
        # data_hora__gte=timezone.now()
        contexto['total_agendamentos'] = Agendamento.objects.filter(
            estagiario=estagiario_logado
        ).count()

        # Evoluções (Filtra evoluções registradas pelo estagiário)
        contexto['total_evolucoes'] = Evolucao.objects.filter(
            estagiario=estagiario_logado
        ).count()

    except ObjectDoesNotExist:
        # Se o usuário logado não estiver cadastrado como Estagiário, a busca falha.
        # Mantemos os totais como zero e a página carrega sem erro 500.
        pass
    
    except Exception as e:
        # Imprime o erro no console. Se você vir um FieldError aqui,
        # o nome do campo de Foreign Key (ex: 'estagiario_responsavel') está errado.
        print(f"Erro de lógica no dashboard do estagiário: {e}") 

    return render(request, 'dashboard_estagiario.html', contexto)