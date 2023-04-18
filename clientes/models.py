from django.db import models
from django.utils.text import slugify

# Create your models here.


class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    cpf = models.CharField(max_length=13)

    def __str__(self) -> str:
        return self.nome


class Carro(models.Model):

    carro = models.CharField(max_length=50)
    placa = models.CharField(max_length=10)
    ano = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    lavagens = models.IntegerField(default=0)
    consertos = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.carro
