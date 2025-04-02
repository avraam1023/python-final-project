from django.shortcuts import render, redirect
from .forms import AuthorCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register_user(request):
    form = AuthorCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'User was successfully registered')
        return redirect('home')

    return render(request, 'core/register.html', {'form': form})

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if user := authenticate(
            request, 
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']):
            login(request, user)
            messages.success(request, 'User was successfully logged in')
            return redirect('home')
        
        messages.error(request, 'Invalid username or password')

    return render(request, 'core/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')
