import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count  
from django.shortcuts import redirect
# Importe os modelos do app atual
from .models import Estagiario, LogAlteracao, AuditoriaAcesso 
from .forms import EstagiarioForm

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
    return redirect('login')

# 3. DASHBOARD DO GESTOR (COM FILTRO, EXPORTAÇÃO E GRÁFICOS)
@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def dashboard_gestor(request):
    # Captura o termo de busca
    usuario_busca = request.GET.get('usuario_busca')
    
    # Querysets base
    logs_queryset = LogAlteracao.objects.all().order_by('-data_hora')
    alertas_queryset = AuditoriaAcesso.objects.filter(sucesso=False).order_by('-data_hora')

    # Aplica o filtro se houver busca
    if usuario_busca:
        logs_queryset = logs_queryset.filter(usuario__username__icontains=usuario_busca)
        alertas_queryset = alertas_queryset.filter(usuario__username__icontains=usuario_busca)

    # Lógica para o Gráfico de Tendência (Alertas por Dia)
    alertas_por_dia = AuditoriaAcesso.objects.filter(sucesso=False).values('data_hora__date').annotate(total=Count('id')).order_by('data_hora__date')

    # Lógica de Exportação para CSV
    if 'exportar' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_auditoria.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Usuario', 'Pagina Tentada', 'Data e Hora'])
        
        for alerta in alertas_queryset:
            writer.writerow([
                alerta.usuario.username, 
                alerta.pagina_tentada, 
                alerta.data_hora.strftime("%d/%m/%Y %H:%M")
            ])
        return response

    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'total_estagiarios': Estagiario.objects.count(),
        'total_agendamentos': Agendamento.objects.count(),
        'total_evolucoes': Evolucao.objects.count(),
        'ultimos_logs': logs_queryset[:5],
        'alertas_seguranca': alertas_queryset[:5],
        'usuario_busca': usuario_busca,
        'alertas_por_dia': alertas_por_dia,  # Enviando dados para o gráfico de linha
    }
    return render(request, 'estagiarios/dashboard_gestor.html', contexto)

# 4. DASHBOARD DO ESTAGIÁRIO
@login_required
def dashboard_estagiario(request):
    return render(request, 'estagiarios/dashboard_estagiario.html')

# --- CRUD ESTAGIÁRIOS ---

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def listar_estagiarios(request):
    busca = request.GET.get('search')
    if busca:
        estagiarios = Estagiario.objects.filter(nome__icontains=busca)
    else:
        estagiarios = Estagiario.objects.all()
    return render(request, 'estagiarios/listar.html', {'estagiarios': estagiarios})

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def cadastrar_estagiario(request):
    if request.method == 'POST':
        form = EstagiarioForm(request.POST)
        if form.is_valid():
            estagiario = form.save()
            LogAlteracao.objects.create(
                usuario=request.user,
                tabela='Estagiario',
                registro_id=estagiario.id,
                acao='CREATE',
                valor_novo=f"Nome: {estagiario.nome}"
            )
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
            messages.success(request, 'Alterações salvas e auditadas!')
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
        messages.success(request, 'Estagiário removido do sistema.')
        return redirect('listar_estagiarios')
    return render(request, 'estagiarios/deletar.html', {'estagiario': estagiario})

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def detalhes_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    return render(request, 'estagiarios/detalhes.html', {'estagiario': estagiario})
def home_redirect(request):
    if request.user.groups.filter(name='Gestores').exists():
        return redirect('dashboard_gestor')
    elif request.user.groups.filter(name='Estagiarios').exists():
        return redirect('dashboard_estagiario')
    return redirect('pagina_inicial')