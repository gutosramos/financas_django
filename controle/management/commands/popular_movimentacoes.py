import os
import django
from django.core.management.base import BaseCommand
from controle.models import Entrada, Saida, Reserva, Movimentacao

class Command(BaseCommand):
    help = 'Popula a tabela Movimentacao com dados existentes'

    def handle(self, *args, **options):
        # Limpar movimentações existentes
        Movimentacao.objects.all().delete()
        
        # Popular com entradas
        for entrada in Entrada.objects.all():
            Movimentacao.objects.create(
                tipo='entrada',
                descricao=entrada.descricao,
                valor=entrada.valor,
                data=entrada.data,
                origem_id=entrada.id
            )
        
        # Popular com saídas
        for saida in Saida.objects.all():
            Movimentacao.objects.create(
                tipo='saida',
                descricao=saida.descricao,
                valor=saida.valor,
                data=saida.data,
                origem_id=saida.id
            )
        
        # Popular com reservas
        for reserva in Reserva.objects.all():
            Movimentacao.objects.create(
                tipo='reserva',
                descricao=reserva.descricao,
                valor=reserva.valor,
                data=reserva.data,
                origem_id=reserva.id
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Populadas {Movimentacao.objects.count()} movimentações')
        )