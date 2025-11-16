from django.shortcuts import render, redirect
from itertools import chain
from operator import attrgetter
from .models import Entrada, Saida
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Entrada, Saida
from datetime import date
from django.urls import reverse

def index(request):
    entradas = Entrada.objects.all()
    saidas = Saida.objects.all()
    extrato = sorted(chain(entradas, saidas), key=attrgetter('data'), reverse=True)
    total_entradas = sum(e.valor for e in entradas) if entradas else 0
    total_saidas = sum(s.valor for s in saidas) if saidas else 0
    saldo = total_entradas - total_saidas
    return render(request, 'index.html', {
        'extrato': extrato,
        'entradas': entradas,
        'saidas': saidas,
        'saldo': saldo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
    })

def nova_entrada(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao','').strip()
        valor = request.POST.get('valor','0').strip()
        data = request.POST.get('data') or timezone.now().date()
        if descricao and valor:
            Entrada.objects.create(descricao=descricao, valor=valor, data=data)
        return redirect('index')
    return render(request, 'nova_entrada.html')

def nova_saida(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao','').strip()
        valor = request.POST.get('valor','0').strip()
        data = request.POST.get('data') or timezone.now().date()
        if descricao and valor:
            Saida.objects.create(descricao=descricao, valor=valor, data=data)
        return redirect('index')
    return render(request, 'nova_saida.html')


def excluir_entrada(request, id):
    entrada = get_object_or_404(Entrada, id=id)
    entrada.delete()
    return redirect('index')

def excluir_saida(request, id):
    saida = get_object_or_404(Saida, id=id)
    saida.delete()
    return redirect('index')

