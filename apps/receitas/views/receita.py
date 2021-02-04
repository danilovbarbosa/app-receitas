from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from receitas.models import Receita


def index(request):
    '''
    Coleta as receitas no BD e apresenta na Index.
    :param request: requisição HTTP.
    :return: render(request, 'receitas/index.html', context=context)
    '''
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    paginator = Paginator(receitas, 6)
    page = request.GET.get('page')
    receita_por_pagina = paginator.get_page(page)

    context: dict = {
        'receitas': receita_por_pagina,
    }

    return render(request, 'receitas/index.html', context=context)


def receita(request, receita_id):
    '''
    Carrega a receita escolhida pelo usuário e apresenta em uma página todos o seu detalhes.
    :param request: requisição HTTP.
    :param receita_id: int.
    :return: render(request, 'receitas/receita.html', receita_a_exibir)
    '''
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita': receita,
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)


def cria_receita(request):
    '''
    Recebe do formulário um conjunto de dados e cria um novo objeto de Receita e salva ele no BD.
    :param request: requisição HTTP.
    :return: redirect('dashboard') ou render(request, 'receitas/cria_receita.html')
    '''
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.id)
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']

        receita = Receita.objects.create(
            pessoa=user,
            nome_receita=nome_receita,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            tempo_de_preparo=tempo_preparo,
            rendimento=rendimento,
            categoria=categoria,
            foto_receita=foto_receita,
            publicada=True,
        )

        return redirect('dashboard')

    return render(request, 'receitas/cria_receita.html')


def deleta_receita(request, receita_id):
    '''
    Deleta do BD a receita indicada no receita_id.
    :param request: requisição HTTP.
    :param receita_id: int.
    :return: redirect('dashboard').
    '''
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def edita_receita(request, receita_id):
    '''
    Edita uma receita selecionada de acordo com receita_id.
    :param request: requisição HTTP.
    :param receita_id: int.
    :return: render(request, 'receitas/edita_receita.html', context=context).
    '''
    receita = get_object_or_404(Receita, pk=receita_id)
    context = {
        'receita': receita,
    }

    return render(request, 'receitas/edita_receita.html', context=context)


def atualiza_receita(request):
    '''
    Atualiza a receita com os dados coletados do formulário.
    :param request: requisição HTTP.
    :return: redirect('dashboard').
    '''
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        receita = Receita.objects.get(pk=receita_id)
        receita.nome_receita = request.POST['nome_receita']
        receita.ingredientes = request.POST['ingredientes']
        receita.modo_preparo = request.POST['modo_preparo']
        receita.tempo_de_preparo = request.POST['tempo_preparo']
        receita.rendimento = request.POST['rendimento']
        receita.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            receita.foto_receita = request.FILES['foto_receita']

        receita.save()

        return redirect('dashboard')
