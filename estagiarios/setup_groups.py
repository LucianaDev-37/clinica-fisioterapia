# estagiarios/setup_groups.py
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from pacientes.models import Paciente
from estagiarios.models import Estagiario
from agendamentos.models import Agendamento
from evolucoes.models import Evolucao

# --- Criar Grupos ---
gestores_group, _ = Group.objects.get_or_create(name='Gestores')
estagiarios_group, _ = Group.objects.get_or_create(name='Estagiarios')

# --- Permissões Gestores ---
# Acesso a estagiarios
ct_estagiario = ContentType.objects.get_for_model(Estagiario)
perm_add_estagiario = Permission.objects.get(codename='add_estagiario', content_type=ct_estagiario)
perm_change_estagiario = Permission.objects.get(codename='change_estagiario', content_type=ct_estagiario)

# Acesso a pacientes
ct_paciente = ContentType.objects.get_for_model(Paciente)
perm_add_paciente = Permission.objects.get(codename='add_paciente', content_type=ct_paciente)
perm_change_paciente = Permission.objects.get(codename='change_paciente', content_type=ct_paciente)
perm_view_paciente = Permission.objects.get(codename='view_paciente', content_type=ct_paciente)

# Acesso a agendamentos
ct_agendamento = ContentType.objects.get_for_model(Agendamento)
perm_add_agendamento = Permission.objects.get(codename='add_agendamento', content_type=ct_agendamento)
perm_change_agendamento = Permission.objects.get(codename='change_agendamento', content_type=ct_agendamento)
perm_view_agendamento = Permission.objects.get(codename='view_agendamento', content_type=ct_agendamento)

# Acesso a evoluções
ct_evolucao = ContentType.objects.get_for_model(Evolucao)
perm_view_evolucao = Permission.objects.get(codename='view_evolucao', content_type=ct_evolucao)

gestores_group.permissions.set([
    perm_add_estagiario, perm_change_estagiario,
    perm_add_paciente, perm_change_paciente, perm_view_paciente,
    perm_add_agendamento, perm_change_agendamento, perm_view_agendamento,
    perm_view_evolucao
])

# --- Permissões Estagiarios ---
estagiarios_group.permissions.set([
    perm_add_paciente, perm_change_paciente, perm_view_paciente,
    perm_add_agendamento, perm_change_agendamento, perm_view_agendamento,
    Permission.objects.get(codename='add_evolucao', content_type=ct_evolucao),
    perm_view_evolucao
])

# --- Criar usuários de teste ---
if not User.objects.filter(username='carlos').exists():
    carlos = User.objects.create_user('carlos', password='senha1234')
    carlos.groups.add(gestores_group)

if not User.objects.filter(username='ana').exists():
    ana = User.objects.create_user('ana', password='senha1234')
    ana.groups.add(estagiarios_group)

print("Grupos, permissões e usuários de teste criados com sucesso!")
