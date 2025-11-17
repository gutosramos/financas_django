from django.core.management.base import BaseCommand
from controle.models import Entrada, Saida, Reserva, Movimentacao

class Command(BaseCommand):
    help = 'Limpa todos os dados do banco PostgreSQL'

    def handle(self, *args, **options):
        # Confirmar antes de deletar
        confirm = input("⚠️  TEM CERTEZA que quer deletar TODOS os dados? (digite 'SIM' para confirmar): ")
        
        if confirm == 'SIM':
            # Deletar na ordem correta para evitar erros de foreign key
            Movimentacao.objects.all().delete()
            Entrada.objects.all().delete()
            Saida.objects.all().delete()
            Reserva.objects.all().delete()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Todos os dados foram deletados!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('❌ Operação cancelada.')
            )