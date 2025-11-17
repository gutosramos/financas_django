from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Entrada, Saida, Reserva, Movimentacao

def index(request):
    # Listas de objetos
    entradas = Entrada.objects.all().order_by('-id')
    saidas = Saida.objects.all().order_by('-id')
    reservas = Reserva.objects.all().order_by('-id')

    # Extrato unificado por data de criação (mais recente primeiro)
    extrato = Movimentacao.objects.all().order_by('-created_at')

    # Totais e saldo
    total_entradas = sum(e.valor for e in entradas)
    total_saidas = sum(s.valor for s in saidas)
    total_reservas = sum(r.valor for r in reservas)
    saldo = total_entradas - total_saidas - total_reservas

    # Abas da interface
    abas = [
        {'id': 'extrato', 'label': 'Extrato'},
        {'id': 'entradas', 'label': 'Entradas'},
        {'id': 'saidas', 'label': 'Saídas'},
        {'id': 'reservas', 'label': 'Reservas'},
    ]

    return render(request, 'index.html', {
        'extrato': extrato,
        'entradas': entradas,
        'saidas': saidas,
        'reservas': reservas,
        'saldo': saldo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total_reservas': total_reservas,
        'abas': abas,
        'now': timezone.localtime(),  # <--- adiciona aqui

    })


def criar_movimentacao(obj, tipo):
    """
    Cria a movimentação correspondente garantindo origem_id.
    """
    from .models import Movimentacao
    Movimentacao.objects.create(
        descricao=obj.descricao,
        valor=obj.valor,
        tipo=tipo,
        data=obj.data,
        origem_id=obj.id
    )


def nova_entrada(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        valor = request.POST.get('valor', '0').strip()
        data = request.POST.get('data') or timezone.now().date()
        if descricao and valor:
            entrada = Entrada.objects.create(descricao=descricao, valor=valor, data=data)
            criar_movimentacao(entrada, 'entrada')
        return redirect('index')
    return render(request, 'nova_entrada.html')


def nova_saida(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        valor = request.POST.get('valor', '0').strip()
        data = request.POST.get('data') or timezone.now().date()
        if descricao and valor:
            saida = Saida.objects.create(descricao=descricao, valor=valor, data=data)
            criar_movimentacao(saida, 'saida')
        return redirect('index')
    return render(request, 'nova_saida.html')


def nova_reserva(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        valor = request.POST.get('valor', '0').strip()
        data = request.POST.get('data') or timezone.now().date()
        if descricao and valor:
            reserva = Reserva.objects.create(descricao=descricao, valor=valor, data=data)
            criar_movimentacao(reserva, 'reserva')
        return redirect('index')
    return render(request, 'nova_reserva.html')


# Funções de exclusão
def excluir_entrada(request, id):
    entrada = get_object_or_404(Entrada, id=id)
    Movimentacao.objects.filter(origem_id=id, tipo='entrada').delete()
    entrada.delete()
    return redirect('index')


def excluir_saida(request, id):
    saida = get_object_or_404(Saida, id=id)
    Movimentacao.objects.filter(origem_id=id, tipo='saida').delete()
    saida.delete()
    return redirect('index')


def excluir_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    Movimentacao.objects.filter(origem_id=id, tipo='reserva').delete()
    reserva.delete()
    return redirect('index')
