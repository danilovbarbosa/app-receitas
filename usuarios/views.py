from django.shortcuts import render, redirect


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if not nome.strip():
            print('O campo não pode ficar em branco.')

        if not email.strip():
            print('O campo não pode ficar em branco.')



        return redirect('login')
    context = {

    }
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

