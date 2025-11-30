from django.contrib.auth.models import Group

def is_gestor(user):
    return user.groups.filter(name='Gestores').exists()

def is_estagiario(user):
    return user.groups.filter(name='Estagiarios').exists()
