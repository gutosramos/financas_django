from django.db import models
from datetime import date

class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('reserva', 'Reserva'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    origem_id = models.IntegerField()  # ID da tabela original (Entrada, Saída ou Reserva)

    def __str__(self):
        return f"{self.data} - {self.tipo} - {self.descricao} - {self.valor}"

class Entrada(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)

    @property
    def tipo(self):
        return "entrada"

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"

class Saida(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)

    @property
    def tipo(self):
        return "saida"

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"

class Reserva(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)

    @property
    def tipo(self):
        return "reserva"

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"
