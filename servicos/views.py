from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.generic import TemplateView, ListView, DetailView, View
from .forms import FormServico
from servicos.models import Servicos
from fpdf import FPDF
from io import BytesIO
# Create your views here.


class NovoServico(TemplateView):
    template_name = 'servicos/novo_servico.html'

    def get(self, request, *args, **kwargs):
        form = FormServico()
        contexto = {
            'form': form
        }
        return render(request, self.template_name, contexto)

    def post(self, request):
        form = FormServico(self.request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        form.save()
        return redirect('servicos:novo_servico')


class ListarServicos(ListView):

    model = Servicos
    template_name = 'servicos/listar_servicos.html'
    context_object_name = 'contexto'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['servicos'] = Servicos.objects.all()
        return contexto


class Servico(View):

    template_name = 'servicos/servico.html'

    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        servico = get_object_or_404(
            Servicos, identificador=kwargs.get('identificador'))
        self.contexto = {
            'servico': servico
        }

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.contexto)


class GerarOS(Servico):

    def get(self, request, *args, **kwargs):
        servico = self.contexto['servico']
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(35, 10, 'Cliente:', 1, 0, 'L', 1)
        pdf.cell(0, 10, f'{servico.cliente.nome}', 1, 1, 'L', 1)
        pdf.cell(35, 10, 'Manutenções: ', 1, 0, 'L', 1)
        # Pelo fato de 1 serviço ter varias categorias, deve-se utilizar o all.
        categoria_manut = servico.categoria_manutencao.all()
        for i, manutencao in enumerate(categoria_manut):
            pdf.cell(
                0, 10, f'- {manutencao.get_titulo_display()}', 1, 1, 'L', 1)
            if not i == len(categoria_manut)-1:
                pdf.cell(35, 10, '', 0, 0)
        pdf.cell(35, 10, 'Data de início: ', 1, 0, 'L', 1)
        pdf.cell(0, 10, f'{servico.data_inicio}', 1, 1, 'L', 1)
        pdf.cell(35, 10, 'Data de entrega: ', 1, 0, 'L', 1)
        pdf.cell(0, 10, f'{servico.data_entrega}', 1, 1, 'L', 1)
        pdf.cell(35, 10, 'Protocolo: ', 1, 0, 'L', 1)
        pdf.cell(0, 10, f'{servico.protocolo}', 1, 1, 'L', 1)

        pd_content = pdf.output(dest='S').encode('latin1')
        pdf_bytes = BytesIO(pd_content)

        return FileResponse(pdf_bytes, as_attachment=True, filename=f'OS-{servico.protocolo}.pdf')
