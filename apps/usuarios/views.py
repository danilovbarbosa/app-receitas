from django.shortcuts import render, redirect
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


def verificar_se_email_e_password_estao_em_branco(request, email, password):
    if email == '':
        messages.error(request, 'O campo e-mail não pode ficar em branco.')
        return True

    if password == '':
        messages.error(request, 'O campo password não pode ficar em branco.')
        return True


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['senha']

        if verificar_se_email_e_password_estao_em_branco(request, email, password):
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



