from django.shortcuts import render, get_object_or_404

from receitas.models import Receita


def index(request):
    receitas = Receita.objects.all()

    context: dict = {
        'receitas': receitas,
    }

    return render(request, 'index.html', context=context)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita': receita,
    }

    return render(request, 'receita.html', receita_a_exibir)
