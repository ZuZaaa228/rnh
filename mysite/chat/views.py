from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *

def index(request):
    return render(request, "chat/home.html",{
        'client_id': request.user.id
    })

# @login_required
def appeal_chat(request, appeal_id):
    appeal = Appeal.objects.get(id=appeal_id)
    messages = Message.objects.filter(appeal=appeal).order_by('time')
    print(appeal_id)
    if request.user.is_admin or request.user == appeal.author:
        return render(request, "chat/room.html", {"appeal_id": appeal_id,
                                                  'appeal': appeal,
                                                  'messages': messages})
    else:
        return redirect('home')

def deactivate_appeal(request, appeal_id):
    appeal = Appeal.objects.get(id=appeal_id)
    form = AppealForm(request.POST, instance=appeal)
    form.save()
    return redirect('room', appeal_id=appeal.id)


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

def create_appeal(request):
    if request.method == 'POST':
        form = AppealForm(request.POST)
        if form.is_valid():
            appeal = form.save(commit=False)
            appeal.author = request.user
            appeal.save()
            return redirect('room', appeal_id=appeal.id)
    else:
        form = AppealForm()
    return render(request, 'chat/create.html', {'form': form})

def user_appeals(request):
    user_appeals_form = UserAppealsForm(user=request.user)
    if request.method == 'POST':
        user_appeals_form = UserAppealsForm(request.POST, user=request.user)
        if user_appeals_form.is_valid():
            selected_appeals = user_appeals_form.cleaned_data['appeals']
            # do something with selected appeals
            return redirect('home')
    return render(request, 'chat/user_appeals.html', {'user_appeals_form': user_appeals_form})