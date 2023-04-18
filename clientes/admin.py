from django.contrib import admin
from clientes.models import Carro, Cliente
# Register your models here.


class CarroAdmin(admin.ModelAdmin):
    model = Carro
    list_display = ('carro', 'placa', 'ano', 'cliente', 'lavagens')


class ClienteAdmin(admin.ModelAdmin):
    model = Cliente
    list_display = ('nome', 'sobrenome', 'cpf', 'email', )


admin.site.register(Carro, CarroAdmin)
admin.site.register(Cliente, ClienteAdmin)
