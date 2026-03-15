from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Estagiario, LogAlteracao, AuditoriaAcesso # <-- Importamos os novos modelos
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
    tem_permissao = user.groups.filter(name='Gestores').exists() or user.is_superuser
    
    # Se o usuário tentou acessar algo restrito e não é gestor, registramos o flagrante
    # Isso ajuda a identificar tentativas de invasão interna
    if user.is_authenticated and not tem_permissao:
        AuditoriaAcesso.objects.create(
            usuario=user,
            pagina_tentada="Área Administrativa/Gestão",
            sucesso=False
        )
    return tem_permissao

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
        return redirect('login')

# 3. DASHBOARD DO GESTOR (BLINDADO)
@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def dashboard_gestor(request):
    # Pegamos os últimos alertas para exibir no painel do gestor
    alertas_seguranca = AuditoriaAcesso.objects.filter(sucesso=False).order_by('-data_hora')[:5]
    
    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'total_estagiarios': Estagiario.objects.count(),
        'total_agendamentos': Agendamento.objects.count(),
        'total_evolucoes': Evolucao.objects.count(),
        'alertas_seguranca': alertas_seguranca,
    }
    return render(request, 'estagiarios/dashboard_gestor.html', contexto)

# 4. DASHBOARD DO ESTAGIÁRIO
@login_required
def dashboard_estagiario(request):
    return render(request, 'estagiarios/dashboard_estagiario.html')

# --- CRUD ESTAGIÁRIOS (COM AUDITORIA ATIVA) ---

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
            estagiario = form.save()
            
            # LOG DE CRIAÇÃO
            LogAlteracao.objects.create(
                usuario=request.user,
                tabela='Estagiario',
                registro_id=estagiario.id,
                acao='CREATE',
                valor_novo=f"Nome: {estagiario.nome}, Matrícula: {estagiario.matricula}"
            )
            
            messages.success(request, 'Estagiário cadastrado e auditado!')
            return redirect('listar_estagiarios')
    else:
        form = EstagiarioForm()
    return render(request, 'estagiarios/form.html', {'form': form})

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def editar_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    if request.method == 'POST':
        # Capturamos o valor antes da alteração para o histórico
        valor_antigo = f"Nome: {estagiario.nome}, Email: {estagiario.email}"
        
        form = EstagiarioForm(request.POST, instance=estagiario)
        if form.is_valid():
            estagiario_editado = form.save()
            
            # LOG DE EDIÇÃO
            LogAlteracao.objects.create(
                usuario=request.user,
                tabela='Estagiario',
                registro_id=estagiario_editado.id,
                acao='UPDATE',
                valor_antigo=valor_antigo,
                valor_novo=f"Nome: {estagiario_editado.nome}, Email: {estagiario_editado.email}"
            )
            
            messages.success(request, 'Estagiário editado e alteração registrada!')
            return redirect('listar_estagiarios')
    else:
        form = EstagiarioForm(instance=estagiario)
    return render(request, 'estagiarios/form.html', {'form': form})

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def deletar_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    if request.method == 'POST':
        # Guardamos os dados antes de apagar para o rastro de segurança
        dados_removidos = f"Nome: {estagiario.nome}, Matrícula: {estagiario.matricula}"
        id_removido = estagiario.id
        
        estagiario.delete()
        
        # LOG DE EXCLUSÃO
        LogAlteracao.objects.create(
            usuario=request.user,
            tabela='Estagiario',
            registro_id=id_removido,
            acao='DELETE',
            valor_antigo=dados_removidos,
            valor_novo="Registro removido permanentemente"
        )
        
        messages.success(request, 'Estagiário removido. Ação auditada.')
        return redirect('listar_estagiarios')
    return render(request, 'estagiarios/deletar.html', {'estagiario': estagiario})

@login_required
@user_passes_test(eh_gestor, login_url='dashboard_estagiario')
def detalhes_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    return render(request, 'estagiarios/detalhes.html', {'estagiario': estagiario})