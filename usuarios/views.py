from datetime import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages

from receitas.models import Receita


def validar_se_nome_email_estao_vazios(request, nome, email):
    if not nome.strip():
        messages.error(request, 'O campo nome não pode ficar em branco.')
        return True

    if not email.strip():
        messages.error(request, 'O campo e-mail não pode ficar em branco.')
        return True

def verificar_igualdade_da_senha(request, password, password2):
    if password != password2:
        messages.error(request, 'As senhas não iguais.')
        return True

def verificar_se_usuario_ja_cadastrado(request, email, nome):
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Usuário já cadastrado com este e-mail.')
        return True

    if User.objects.filter(username=nome).exists():
        messages.error(request, 'Usuário já cadastrado.')
        return True


def validar_dados(request, nome, email, password, password2):
    if (
            validar_se_nome_email_estao_vazios(request, nome, email) or
            verificar_igualdade_da_senha(request, password, password2) or
            verificar_se_usuario_ja_cadastrado(request, email, nome)
    ):
        return True

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if validar_dados(request, nome, email, password, password2):
            return redirect('cadastro')

        usuario: User = User.objects.create_user(username=nome, email=email, password=password)
        usuario.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
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
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
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
