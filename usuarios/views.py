from datetime import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth

from receitas.models import Receita


def validar_nome_email(nome, email):
    if not nome.strip():
        print('O campo não pode ficar em branco.')
        return redirect('cadastro')

    if not email.strip():
        print('O campo não pode ficar em branco.')
        return redirect('cadastro')

def verificar_igualdade_da_senha(password, password2):
    if password != password2:
        print('As senhas não iguais.')
        return redirect('cadastro')

def verificar_se_usuario_ja_cadastrado(email):
    if User.objects.filter(email=email).exists():
        print('Usuário já cadastrado.')
        return redirect('cadastro')


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        validar_nome_email(nome, email)
        verificar_igualdade_da_senha(password, password2)
        verificar_se_usuario_ja_cadastrado(email)

        usuario: User = User.objects.create_user(username=nome, email=email, password=password)
        usuario.save()

        return redirect('login')
    context = {}
    return render(request, 'usuarios/cadastro.html', context=context)


def verificar_se_email_e_password_estao_em_branco(email, password):
    if email == '' or password == '':
        return redirect('login')

    else:
        return redirect('dashboard')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['senha']

        if email == '' or password == '':
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    return render(request, 'usuarios/login.html')

def dashboard(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.all()
        context = {
            'receitas': receitas,
        }
        return render(request, 'usuarios/dashboard.html', context=context)
    else:
        return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('index')


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

    return render(request, 'usuarios/cria_receita.html')
