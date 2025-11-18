from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('reserva', 'Reserva'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # <-- FALTAVA AQUI!

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    origem_id = models.IntegerField()  # ID da entrada/saida/reserva original

    def __str__(self):
        return f"{self.data} - {self.tipo} - {self.descricao} - {self.valor}"


class Entrada(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)

    @property
    def tipo(self):
        return "entrada"

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"


class Saida(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)

    @property
    def tipo(self):
        return "saida"

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"


class Reserva(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)

    @property
    def tipo(self):
        return "reserva"

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"
