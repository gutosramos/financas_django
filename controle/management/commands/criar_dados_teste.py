from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from controle.models import Entrada, Saida, Reserva, Movimentacao

class Command(BaseCommand):
    help = 'Cria dados de teste para diferentes meses'

    def handle(self, *args, **options):
        # Limpar dados existentes
        Movimentacao.objects.all().delete()
        Entrada.objects.all().delete()
        Saida.objects.all().delete()
        Reserva.objects.all().delete()
        
        # Dados para meses diferentes
        meses_teste = [
            (2025, 11),  # Mês atual
            (2025, 10),  # Mês anterior
            (2025, 9),   # Dois meses atrás
        ]
        
        for ano, mes in meses_teste:
            # Entradas
            for i in range(3):
                entrada = Entrada.objects.create(
                    descricao=f"Salário {mes}/{ano}",
                    valor=1500 + (i * 100),
                    data=datetime(ano, mes, 15)
                )
                Movimentacao.objects.create(
                    tipo='entrada',
                    descricao=entrada.descricao,
                    valor=entrada.valor,
                    data=entrada.data,
                    origem_id=entrada.id
                )
            
            # Saídas
            for i in range(2):
                saida = Saida.objects.create(
                    descricao=f"Conta {mes}/{ano}",
                    valor=200 + (i * 50),
                    data=datetime(ano, mes, 10)
                )
                Movimentacao.objects.create(
                    tipo='saida',
                    descricao=saida.descricao,
                    valor=saida.valor,
                    data=saida.data,
                    origem_id=saida.id
                )
            
            # Reservas
            reserva = Reserva.objects.create(
                descricao=f"Reserva {mes}/{ano}",
                valor=300,
                data=datetime(ano, mes, 5)
            )
            Movimentacao.objects.create(
                tipo='reserva',
                descricao=reserva.descricao,
                valor=reserva.valor,
                data=reserva.data,
                origem_id=reserva.id
            )
        
        self.stdout.write(
            self.style.SUCCESS('Dados de teste criados para diferentes meses!')
        )