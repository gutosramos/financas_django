from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Entrada, Saida, Reserva, Movimentacao

def criar_movimentacao(obj, tipo):
    """
    Cria a movimentação correspondente garantindo origem_id.
    """
    Movimentacao.objects.create(
        descricao=obj.descricao,
        valor=obj.valor,
        tipo=tipo,
        data=obj.data,
        origem_id=obj.id
    )

@login_required
def index(request):
    # Obter mês selecionado ou usar o atual
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
    
    # Calcular datas
    primeiro_dia = datetime(ano, mes, 1).date()
    if mes == 12:
        ultimo_dia = datetime(ano, mes, 31).date()
    else:
        ultimo_dia = datetime(ano, mes + 1, 1).date() - timedelta(days=1)
    
    # Filtros para o mês selecionado
    movimentacoes_mes = Movimentacao.objects.filter(
        data__range=[primeiro_dia, ultimo_dia]
    )
    
    entradas_mes = movimentacoes_mes.filter(tipo='entrada')
    saidas_mes = movimentacoes_mes.filter(tipo='saida')
    reservas_mes = movimentacoes_mes.filter(tipo='reserva')
    
    total_entradas_mes = entradas_mes.aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_mes = saidas_mes.aggregate(Sum('valor'))['valor__sum'] or 0
    total_reservas_mes = reservas_mes.aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_mes = total_entradas_mes - total_saidas_mes - total_reservas_mes
    
    # Dados totais (todos os meses)
    total_entradas_geral = Movimentacao.objects.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_geral = Movimentacao.objects.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0
    total_reservas_geral = Movimentacao.objects.filter(tipo='reserva').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_geral = total_entradas_geral - total_saidas_geral - total_reservas_geral
    
    # CORREÇÃO: Buscar os objetos ORIGINAIS para ter acesso aos IDs reais
    extrato = []
    for mov in movimentacoes_mes.order_by('-data', '-created_at'):
        # Buscar o objeto original baseado no tipo e origem_id
        if mov.tipo == 'entrada':
            try:
                obj_original = Entrada.objects.get(id=mov.origem_id)
                item_id = obj_original.id
            except Entrada.DoesNotExist:
                item_id = None
        elif mov.tipo == 'saida':
            try:
                obj_original = Saida.objects.get(id=mov.origem_id)
                item_id = obj_original.id
            except Saida.DoesNotExist:
                item_id = None
        elif mov.tipo == 'reserva':
            try:
                obj_original = Reserva.objects.get(id=mov.origem_id)
                item_id = obj_original.id
            except Reserva.DoesNotExist:
                item_id = None
        else:
            item_id = None
        
        extrato.append({
            'id': item_id,  # ID REAL do objeto original
            'tipo': mov.tipo,
            'descricao': mov.descricao,
            'valor': mov.valor,
            'data': mov.data,
            'origem_id': mov.origem_id  # Mantém também para referência
        })
    
    # Lista de meses disponíveis para filtro
    meses_disponiveis = []
    todos_meses = Movimentacao.objects.dates('data', 'month', order='DESC')[:12]
    
    for data in todos_meses:
        meses_disponiveis.append({
            'valor': data.strftime('%Y-%m'),
            'label': data.strftime('%B/%Y').title()
        })
    
    context = {
        # Dados do mês
        'mes_atual': f"{primeiro_dia.strftime('%B/%Y').title()}",
        'total_entradas': total_entradas_mes,
        'total_saidas': total_saidas_mes,
        'total_reservas': total_reservas_mes,
        'saldo': saldo_mes,
        
        # Dados gerais
        'total_entradas_geral': total_entradas_geral,
        'total_saidas_geral': total_saidas_geral,
        'total_reservas_geral': total_reservas_geral,
        'saldo_geral': saldo_geral,
        
        # Dados para abas
        'extrato': extrato,
        'entradas': [e for e in extrato if e['tipo'] == 'entrada'],
        'saidas': [e for e in extrato if e['tipo'] == 'saida'],
        'reservas': [e for e in extrato if e['tipo'] == 'reserva'],
        
        # Filtros
        'mes_selecionado': f"{ano}-{mes:02d}",
        'meses_disponiveis': meses_disponiveis,
        
        # Abas
        'abas': [
            {'id': 'extrato', 'label': 'Extrato'},
            {'id': 'entradas', 'label': 'Entradas'},
            {'id': 'saidas', 'label': 'Saídas'},
            {'id': 'reservas', 'label': 'Reservas'},
        ]
    }
    return render(request, 'index.html', context)

@login_required
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

@login_required
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

@login_required
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

# Funções de exclusão (JÁ ESTÃO CORRETAS)
@login_required
def excluir_entrada(request, id):
    entrada = get_object_or_404(Entrada, id=id)
    Movimentacao.objects.filter(origem_id=id, tipo='entrada').delete()
    entrada.delete()
    return redirect('index')

@login_required
def excluir_saida(request, id):
    saida = get_object_or_404(Saida, id=id)
    Movimentacao.objects.filter(origem_id=id, tipo='saida').delete()
    saida.delete()
    return redirect('index')

@login_required
def excluir_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    Movimentacao.objects.filter(origem_id=id, tipo='reserva').delete()
    reserva.delete()
    return redirect('index')

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')