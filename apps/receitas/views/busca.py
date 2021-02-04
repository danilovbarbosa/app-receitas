from django.shortcuts import render

from receitas.models import Receita


def busca(request):
    '''
    Busca receitas de acordo com a string informada no formulário.
    :param request: requisição HTTP.
    :return: render(request, 'receitas/buscar.html', context=context)
    '''
    lista_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    context: dict = {
        'receitas': lista_receitas,
    }

    return render(request, 'receitas/buscar.html', context=context)