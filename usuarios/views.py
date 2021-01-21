from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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

def login(request):
    context = {

    }
    return render(request, 'usuarios/login.html', context=context)

def dashboard(request):
    context = {

    }
    return render(request, 'usuarios/dashboard.html', context=context)

def logout(request):
    context = {

    }
    return render(request, 'usuarios/cadastro.html', context=context)

