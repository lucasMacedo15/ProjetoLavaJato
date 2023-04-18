from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    path('', views.Clientes.as_view(), name='clientes'),
    path('atualiza_cliente/', views.AtualizaCliente.as_view(),
         name='atualiza_cliente'),
    path('update_carro/<int:id>', views.UpdateCarro.as_view(),
         name='update_carro'),
    path('excluir_carro/<int:id>', views.ExcluirCarro.as_view(),
         name='excluir_carro'),
    path('update_cliente/<int:id>', views.UpdateCliente.as_view(),
         name='update_cliente'),

]
