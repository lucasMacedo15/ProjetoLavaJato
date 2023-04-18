from django.forms import ModelForm
from .models import Servicos, CategoriaManutencao


class FormServico(ModelForm):
    class Meta:
        model = Servicos
        exclude = ['finalizado', 'protocolo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for titulo, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': titulo})
        choices = list()
        for i, j in self.fields['categoria_manutencao'].choices:
            categoria = CategoriaManutencao.objects.get(titulo=j)
            choices.append((i.value, categoria.get_titulo_display()))

        self.fields['categoria_manutencao'].choices = choices
