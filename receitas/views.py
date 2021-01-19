from django.shortcuts import render

def index(request):
    receitas: dict = {
        1: 'Lasanha',
        2: 'Sopa de legumes',
        3: 'Soverte',
        4: 'Bolo de chocolate',
    }
    context: dict = {
        'nome_das_receitas': receitas,
    }

    return render(request, 'index.html', context=context)


def receita(request):
    return render(request, 'receita.html')