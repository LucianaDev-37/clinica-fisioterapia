import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count  # Importado apenas uma vez aqui

# Importação dos seus modelos
from agendamentos.models import Agendamento
from pacientes.models import Paciente
from estagiarios.models import Estagiario, LogAlteracao, AuditoriaAcesso
from evolucoes.models import Evolucao

# Função auxiliar para verificar se é gestor
def eh_gestor(user):
    return user.groups.filter(name='Gestores').exists()

# 1. Ajuste na Página Inicial
def pagina_inicial(request):
    if request.user.is_authenticated:
        return redirecionar_dashboard(request)
    return render(request, 'pagina_inicial.html')

# 2. O seu "Guarda de Trânsito"
def redirecionar_dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if eh_gestor(user):
        return redirect('dashboard_gestor')
    if user.groups.filter(name='Estagiarios').exists():
        return redirect('dashboard_estagiario')
    return redirect('login')

# 3. Dashboard do Gestor (Lógica Única e Corrigida)
@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def dashboard_gestor(request):
    # --- Lógica de Busca ---
    usuario_busca = request.GET.get('usuario_busca')
    logs_queryset = LogAlteracao.objects.all().order_by('-data_hora')
    alertas_queryset = AuditoriaAcesso.objects.filter(sucesso=False).order_by('-data_hora')

    if usuario_busca:
        logs_queryset = logs_queryset.filter(usuario__username__icontains=usuario_busca)
        alertas_queryset = alertas_queryset.filter(usuario__username__icontains=usuario_busca)

    # --- Lógica de Exportação para CSV ---
    if 'exportar' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_auditoria.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Usuario', 'Pagina Tentada', 'Data e Hora'])
        
        for alerta in alertas_queryset:
            # Corrigido para %M (minutos)
            data_formatada = alerta.data_hora.strftime("%d/%m/%Y %H:%M")
            writer.writerow([alerta.usuario.username, alerta.pagina_tentada, data_formatada])
        
        return response

    # --- Dados para o Gráfico de Linha (Tendência) ---
    alertas_por_dia = AuditoriaAcesso.objects.filter(sucesso=False)\
        .values('data_hora__date')\
        .annotate(total=Count('id'))\
        .order_by('data_hora__date')

    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'total_estagiarios': Estagiario.objects.count(),
        'total_agendamentos': Agendamento.objects.count(),
        'total_evolucoes': Evolucao.objects.count(),
        'ultimos_logs': logs_queryset[:5],
        'alertas_seguranca': alertas_queryset[:5],
        'alertas_por_dia': alertas_por_dia, 
        'usuario_busca': usuario_busca,
    }
    return render(request, 'dashboard_gestor.html', contexto)

# 4. Dashboard do Estagiário
@login_required
def dashboard_estagiario(request):
    user = request.user
    contexto = {'total_pacientes': 0, 'total_agendamentos': 0, 'total_evolucoes': 0}
    try:
        estagiario_logado = Estagiario.objects.get(user=user)
        contexto['total_pacientes'] = Paciente.objects.filter(estagiario_responsavel=estagiario_logado).count()
        contexto['total_agendamentos'] = Agendamento.objects.filter(estagiario=estagiario_logado).count()
        contexto['total_evolucoes'] = Evolucao.objects.filter(estagiario=estagiario_logado).count()
    except ObjectDoesNotExist:
        pass
    return render(request, 'dashboard_estagiario.html', contexto)