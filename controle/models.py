from django.db import models
from datetime import date
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
