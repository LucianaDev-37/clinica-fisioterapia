from django.shortcuts import render, redirect, get_object_or_404
from .models import Evolucao
from .forms import EvolucaoForm

def listar_evolucoes(request):
    evolucoes = Evolucao.objects.all().order_by('-data')
    return render(request, 'evolucoes/listar.html', {'evolucoes': evolucoes})


def cadastrar_evolucao(request):
    if request.method == 'POST':
        form = EvolucaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_evolucoes')
    else:
        form = EvolucaoForm()

    return render(request, 'evolucoes/cadastrar.html', {'form': form})


def editar_evolucao(request, id):
    evolucao = get_object_or_404(Evolucao, id=id)

    if request.method == 'POST':
        form = EvolucaoForm(request.POST, instance=evolucao)
        if form.is_valid():
            form.save()
            return redirect('listar_evolucoes')
    else:
        form = EvolucaoForm(instance=evolucao)

    return render(request, 'evolucoes/editar.html', {'form': form, 'evolucao': evolucao})


def deletar_evolucao(request, id):
    evolucao = get_object_or_404(Evolucao, id=id)

    if request.method == 'POST':
        evolucao.delete()
        return redirect('listar_evolucoes')

    return render(request, 'evolucoes/deletar.html', {'evolucao': evolucao})
