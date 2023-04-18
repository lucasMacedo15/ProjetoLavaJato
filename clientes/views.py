from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import View, DetailView, DeleteView, UpdateView, ListView
from .models import Cliente, Carro
import re
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
# Create your views here.


class Clientes(ListView):
    template_name = 'clientes/clientes.html'

    def get(self, request, *args, **kwargs):
        contexto = {
            'clientes': Cliente.objects.all()
        }
        return render(self.request, self.template_name, contexto)

    def post(self, request, *args, **kwargs):
        # CLIENTE

        nome = self.request.POST.get('nome')
        sobrenome = self.request.POST.get('sobrenome')
        email = self.request.POST.get('email')
        cpf = self.request.POST.get('cpf')
        # CARROS
        carros = self.request.POST.getlist('carro')
        placas = self.request.POST.getlist('placa')
        anos = self.request.POST.getlist('ano')
        carro_zipado = zip(carros, placas, anos)
        # FILTRA CLIENTES
        cliente = Cliente.objects.filter(cpf=cpf).first()
        # VERIFICA SE EXISTE CLIENTE E GERA CONTEXTO
        if cliente:
            contexto = {
                'nome': nome,
                'cpf': sobrenome,
                'email': email,
                'carros': carro_zipado
            }
            return render(self.request, self.template_name, contexto)
        # VALIDAÇÃO E MAIL COM RE
        # if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
        #     return HttpResponse('Email inválido')

        cliente = Cliente(
            nome=nome, sobrenome=sobrenome, email=email, cpf=cpf
        )
        cliente.save()

        for carro, placa, ano in carro_zipado:
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()

        return redirect('cliente:clientes')


class AtualizaCliente(View):
    def post(self, request, *args, **kwargs):
        # Id cliente capturado do front
        id_cliente = request.POST.get('id_cliente')
        if not id_cliente:
            return redirect('cliente:clientes')
        # Filtro do cliente da DB
        cliente = Cliente.objects.filter(id=id_cliente)

        carros = Carro.objects.filter(cliente=cliente.first())

        # Serialização do cliente em json. Obs: O cliente deve ser QuerySet Obs²: Carregar como json
        carros_json = json.loads(serializers.serialize('json', carros))
        carros_json = [{'fields': carro['fields'], 'id':carro['pk']}
                       for carro in carros_json]
        cliente_json = json.loads(serializers.serialize('json', cliente))[
            0]['fields']
        cliente_id_json = json.loads(serializers.serialize('json', cliente))[
            0]['pk']

        data = {'cliente': cliente_json, 'carros': carros_json,
                'cliente_id': cliente_id_json, }

        # Retorno dos dados para front
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateCarro(DetailView):
    model = Carro

    def post(self, request, id, *args, **kwargs):

        nome_carro = request.POST.get('carro')
        placa = request.POST.get('placa')
        ano = request.POST.get('ano')
        carro = Carro.objects.get(id=id)
        # Filtre carros pela placa recebida e exclua ele mesmo. Caso retorne algo na Query set
        # Cairá na condição de placa existente
        list_carros = Carro.objects.exclude(id=id).filter(placa=placa)

        print(list_carros)
        if list_carros.exists():
            return HttpResponse('placa já existente')
        carro.carro = nome_carro
        carro.placa = placa
        carro.ano = ano
        carro.save()
        return redirect(reverse('cliente:clientes')+f'?aba=att_cliente&id_cliente={id}')


class ExcluirCarro(DeleteView):
    model = Carro

    def get(self, request, id, *args, **kwargs) -> HttpResponse:

        carro = get_object_or_404(Carro, id=id)
        carro.delete()

        return redirect(reverse('cliente:clientes')+f'?aba=att_cliente&id_cliente={id}')


class UpdateCliente(View):

    def post(self, request, id, *args, **kwargs) -> HttpResponse:
        # Os dados vindos do body vem como bytes, sendo assim: carregue-os como string json
        corpo = json.loads(self.request.body)
        cliente = get_object_or_404(Cliente, id=id)
        nome = corpo['nome']
        sobrenome = corpo['sobrenome']
        cpf = corpo['cpf']
        email = corpo['email']
        try:
            cliente.nome = nome
            cliente.sobrenome = sobrenome
            cliente.cpf = cpf
            cliente.email = email
            cliente.save()

            return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'email': email, })
        except:
            return JsonResponse({'status': '500'})
