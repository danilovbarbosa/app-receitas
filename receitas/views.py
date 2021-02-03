from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages

from receitas.models import Receita


def index(request):
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)

    context: dict = {
        'receitas': receitas,
    }

    return render(request, 'receitas/index.html', context=context)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita': receita,
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)


def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']

        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    context: dict = {
        'receitas': lista_receitas,
    }

    return render(request, 'receitas/buscar.html', context=context)


def cria_receita(request):
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
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    context = {
        'receita': receita,
    }

    return render(request, 'receitas/edita_receita.html', context=context)


def atualiza_receita(request):
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
