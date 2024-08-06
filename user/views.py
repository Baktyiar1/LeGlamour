from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from .forms import RegisterUserForm, LoginUserForm


def register_views(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('index')
        for key, error in form.errors.items():
            for err in error:
                messages.error(request, f'{err}')
    else:
        form = RegisterUserForm()
    return render(request, 'user/register.html', {'form': form})


def login_views(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('index')
        else:
            for key, error in form.errors.items():
                for err in error:
                    messages.error(request, f'{err}')
    else:
        form = LoginUserForm()
    return render(request, 'user/login.html', {'form': form})


def logout_views(request):
    logout(request)
    messages.success(request, 'Вы успешено вышли из системы.')
    return redirect('index')
