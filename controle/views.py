from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Entrada, Saida, Reserva, Movimentacao


def criar_movimentacao(obj, tipo, user):
    """
    Cria a movimentação garantido o vínculo com o usuário.
    """
    Movimentacao.objects.create(
        descricao=obj.descricao,
        valor=obj.valor,
        tipo=tipo,
        data=obj.data,
        origem_id=obj.id,
        user=user
    )


@login_required
def index(request):

    user = request.user  # <<< USUÁRIO LOGADO

    # Filtrar apenas dados do usuário
    entradas = Entrada.objects.filter(user=user)
    saidas = Saida.objects.filter(user=user)
    reservas = Reserva.objects.filter(user=user)

    # Obter mês selecionado
    mes_selecionado = request.GET.get('mes')
    if mes_selecionado:
        try:
            data_filtro = datetime.strptime(mes_selecionado, '%Y-%m')
            ano = data_filtro.year
            mes = data_filtro.month
        except:
            ano = timezone.now().year
            mes = timezone.now().month
    else:
        ano = timezone.now().year
        mes = timezone.now().month
    
    # Intervalo
    primeiro_dia = datetime(ano, mes, 1).date()
    if mes == 12:
        ultimo_dia = datetime(ano, 12, 31).date()
    else:
        ultimo_dia = datetime(ano, mes + 1, 1).date() - timedelta(days=1)
    
    # Movimentações APENAS do usuário
    movimentacoes_mes = Movimentacao.objects.filter(
        user=user,
        data__range=[primeiro_dia, ultimo_dia]
    )

    # Totais do mês
    entradas_mes = movimentacoes_mes.filter(tipo='entrada')
    saidas_mes = movimentacoes_mes.filter(tipo='saida')
    reservas_mes = movimentacoes_mes.filter(tipo='reserva')

    total_entradas_mes = entradas_mes.aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_mes = saidas_mes.aggregate(Sum('valor'))['valor__sum'] or 0
    total_reservas_mes = reservas_mes.aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_mes = total_entradas_mes - total_saidas_mes - total_reservas_mes

    # Totais gerais (só do user)
    total_entradas_geral = Movimentacao.objects.filter(user=user, tipo='entrada').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_geral = Movimentacao.objects.filter(user=user, tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0
    total_reservas_geral = Movimentacao.objects.filter(user=user, tipo='reserva').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_geral = total_entradas_geral - total_saidas_geral - total_reservas_geral

    # Extrato com ID verdadeiro de origem
    extrato = []
    for mov in movimentacoes_mes.order_by('-data', '-created_at'):

        item_id = None

        if mov.tipo == 'entrada':
            try:
                item_id = Entrada.objects.get(id=mov.origem_id, user=user).id
            except Entrada.DoesNotExist:
                item_id = None

        elif mov.tipo == 'saida':
            try:
                item_id = Saida.objects.get(id=mov.origem_id, user=user).id
            except Saida.DoesNotExist:
                item_id = None

        elif mov.tipo == 'reserva':
            try:
                item_id = Reserva.objects.get(id=mov.origem_id, user=user).id
            except Reserva.DoesNotExist:
                item_id = None

        extrato.append({
            'id': item_id,
            'tipo': mov.tipo,
            'descricao': mov.descricao,
            'valor': mov.valor,
            'data': mov.data,
            'origem_id': mov.origem_id
        })

    # Meses disponíveis (só os do user)
    meses_disponiveis = []
    todos_meses = Movimentacao.objects.filter(user=user).dates('data', 'month', order='DESC')[:12]
    
    for data in todos_meses:
        meses_disponiveis.append({
            'valor': data.strftime('%Y-%m'),
            'label': data.strftime('%B/%Y').title()
        })
    
    context = {
        'mes_atual': f"{primeiro_dia.strftime('%B/%Y').title()}",
        'total_entradas': total_entradas_mes,
        'total_saidas': total_saidas_mes,
        'total_reservas': total_reservas_mes,
        'saldo': saldo_mes,

        'total_entradas_geral': total_entradas_geral,
        'total_saidas_geral': total_saidas_geral,
        'total_reservas_geral': total_reservas_geral,
        'saldo_geral': saldo_geral,

        'extrato': extrato,
        'entradas': [e for e in extrato if e['tipo'] == 'entrada'],
        'saidas': [e for e in extrato if e['tipo'] == 'saida'],
        'reservas': [e for e in extrato if e['tipo'] == 'reserva'],

        'mes_selecionado': f"{ano}-{mes:02d}",
        'meses_disponiveis': meses_disponiveis,

        'abas': [
            {'id': 'extrato', 'label': 'Extrato'},
            {'id': 'entradas', 'label': 'Entradas'},
            {'id': 'saidas', 'label': 'Saídas'},
            {'id': 'reservas', 'label': 'Reservas'},
        ]
    }
    return render(request, 'index.html', context)


# ====== CRIAÇÃO ======

@login_required
def nova_entrada(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        valor = request.POST.get('valor', '0').strip()
        data = request.POST.get('data') or timezone.now().date()

        if descricao and valor:
            entrada = Entrada.objects.create(
                descricao=descricao,
                valor=valor,
                data=data,
                user=request.user
            )
            criar_movimentacao(entrada, 'entrada', request.user)

        return redirect('index')

    return render(request, 'nova_entrada.html')


@login_required
def nova_saida(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        valor = request.POST.get('valor', '0').strip()
        data = request.POST.get('data') or timezone.now().date()

        if descricao and valor:
            saida = Saida.objects.create(
                descricao=descricao,
                valor=valor,
                data=data,
                user=request.user
            )
            criar_movimentacao(saida, 'saida', request.user)

        return redirect('index')

    return render(request, 'nova_saida.html')


@login_required
def nova_reserva(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        valor = request.POST.get('valor', '0').strip()
        data = request.POST.get('data') or timezone.now().date()

        if descricao and valor:
            reserva = Reserva.objects.create(
                descricao=descricao,
                valor=valor,
                data=data,
                user=request.user
            )
            criar_movimentacao(reserva, 'reserva', request.user)

        return redirect('index')

    return render(request, 'nova_reserva.html')


# ====== EXCLUSÕES SEGURAS ======

@login_required
def excluir_entrada(request, id):
    entrada = get_object_or_404(Entrada, id=id, user=request.user)
    Movimentacao.objects.filter(origem_id=id, tipo='entrada', user=request.user).delete()
    entrada.delete()
    return redirect('index')


@login_required
def excluir_saida(request, id):
    saida = get_object_or_404(Saida, id=id, user=request.user)
    Movimentacao.objects.filter(origem_id=id, tipo='saida', user=request.user).delete()
    saida.delete()
    return redirect('index')


@login_required
def excluir_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id, user=request.user)
    Movimentacao.objects.filter(origem_id=id, tipo='reserva', user=request.user).delete()
    reserva.delete()
    return redirect('index')


@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')
