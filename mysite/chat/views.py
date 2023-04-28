from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Appeal
from .forms import *

def index(request):
    return render(request, "chat/home.html",{
        'client_id': request.user.id
    })

# @login_required
def appeal_chat(request, client_id):
    return render(request, "chat/room.html", {"client_id": client_id})


def login_view(request):
    if request.user.id != None:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'chat/login.html', context=context)

def register_view(request):
    if request.user.id != None:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'chat/register.html', context=context)