from django.shortcuts import render

from receitas.models import Receita


def index(request):
    receitas = Receita.objects.all()

    context: dict = {
        'receitas': receitas,
    }

    return render(request, 'index.html', context=context)


def receita(request):
    return render(request, 'receita.html')