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
    from .models import Movimentacao
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
    
    # CORREÇÃO: Calcular datas SIMPLES e CORRETAS
    primeiro_dia = datetime(ano, mes, 1).date()  # Primeiro dia do mês como date
    if mes == 12:
        ultimo_dia = datetime(ano, mes, 31).date()  # Último dia de dezembro
    else:
        ultimo_dia = datetime(ano, mes + 1, 1).date() - timedelta(days=1)  # Último dia do mês
    
    print(f"DEBUG: Filtrando de {primeiro_dia} até {ultimo_dia}")  # Log para debug
    
    # Filtros para o mês selecionado - CORREÇÃO
    movimentacoes_mes = Movimentacao.objects.filter(
        data__range=[primeiro_dia, ultimo_dia]  # Usando range para ser mais preciso
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
    
    # Preparar dados para as abas
    extrato = []
    for mov in movimentacoes_mes.order_by('-data', '-created_at'):
        extrato.append({
            'tipo': mov.tipo,
            'descricao': mov.descricao,
            'valor': mov.valor,
            'data': mov.data,
            'origem_id': mov.origem_id
        })
    
    # Lista de meses disponíveis para filtro
    meses_disponiveis = []
    
    # Pegar meses de TODAS as movimentações
    todos_meses = Movimentacao.objects.dates('data', 'month', order='DESC')[:12]
    
    for data in todos_meses:
        meses_disponiveis.append({
            'valor': data.strftime('%Y-%m'),
            'label': data.strftime('%B/%Y').title()
        })
    
    context = {
        # Dados do mês
        'mes_atual': f"{primeiro_dia.strftime('%B/%Y').title()}",
        'primeiro_dia': primeiro_dia,  # Para debug
        'ultimo_dia': ultimo_dia,      # Para debug
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

# ... o resto das views permanece igual ...

@login_required


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


# Funções de exclusão
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