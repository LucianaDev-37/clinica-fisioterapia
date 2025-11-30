from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Estagiario
from .forms import EstagiarioForm

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
        return redirect('login')

# -------------------------------
# PAINÉIS
# -------------------------------
@login_required
def painel_gestores(request):
    return HttpResponse("Painel do Gestor")

@login_required
def painel_estagiarios(request):
    return HttpResponse("Painel do Estagiário")

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
            return redirect('listar_estagiarios')
    else:
        form = EstagiarioForm(instance=estagiario)
    return render(request, 'estagiarios/form.html', {'form': form})

def deletar_estagiario(request, id):
    estagiario = get_object_or_404(Estagiario, id=id)
    if request.method == 'POST':
        estagiario.delete()
        return redirect('listar_estagiarios')
    return render(request, 'estagiarios/deletar.html', {'estagiario': estagiario})
