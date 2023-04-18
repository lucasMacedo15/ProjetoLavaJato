from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('novo_servico/', views.NovoServico.as_view(), name='novo_servico'),
    path('listar_servicos/', views.ListarServicos.as_view(), name='listar_servicos'),
    path('servico/<str:identificador>', views.Servico.as_view(), name='servico'),
    path('gerar_os/<str:identificador>',
         views.GerarOS.as_view(), name='gerar_os'),


]
